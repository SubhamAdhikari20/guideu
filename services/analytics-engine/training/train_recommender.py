"""Train + evaluate the content-based route recommender.

The "model" is an interpretable artifact: a per-route feature/popularity profile
plus the scoring weights. Popularity is computed from the **train** period only
(no leakage). Offline evaluation ranks routes for each 2024 user and scores the
ranking against the routes they actually booked/completed (Precision@K, NDCG@K),
with a popularity-only baseline for comparison.
"""
from __future__ import annotations

import logging

import numpy as np
import pandas as pd

from data.loader import load_interactions, load_routes, load_tourists
from evaluation.metrics import ndcg_at_k, precision_at_k
from features.recommender import BUDGET_USD, DEFAULT_WEIGHTS, build_route_profile, budget_fit
from registry import save_model

logger = logging.getLogger("guideu.ml.train.recommender")

ARTIFACT_COLS = [
    "route_id", "route_name", "region", "difficulty", "difficulty_norm",
    "best_seasons", "estimated_cost_usd", "popularity",
]
MAX_EVAL_USERS = 3000


def _evaluate(profile: pd.DataFrame, train_inter: pd.DataFrame, test_inter: pd.DataFrame) -> dict:
    route_ids = profile["route_id"].to_numpy()
    diff_norm = profile["difficulty_norm"].to_numpy(dtype=float)
    pop = profile["popularity"].to_numpy(dtype=float)
    cost = profile["estimated_cost_usd"].to_numpy(dtype=float)
    w = DEFAULT_WEIGHTS

    # Pre-compute the budget-fit vector for each band (only 4 distinct values).
    budget_vectors = {band: np.array([budget_fit(c, band) for c in cost]) for band in BUDGET_USD}
    default_budget = np.full(len(cost), 0.7)

    # Relevant routes per user in the test period (positive feedback only).
    rel = test_inter[(test_inter["item_type"] == "Route") & (test_inter["interaction_type"].isin(["Book", "Complete"]))]
    relevant = rel.groupby("tourist_id")["item_id"].agg(set)

    survey = load_tourists().set_index("tourist_id")[["pref_adventure_score", "budget_band"]]

    eval_users = [u for u in relevant.index if u in survey.index][:MAX_EVAL_USERS]
    if not eval_users:
        return {"n_eval_users": 0}

    # Popularity-only baseline ranking (same for every user).
    pop_top = list(route_ids[np.argsort(-pop)][:10])

    p5, n5, hr10, base_hr10 = [], [], [], []
    base_top10 = set(pop_top)
    for user in eval_users:
        adv = float(survey.at[user, "pref_adventure_score"])
        band = survey.at[user, "budget_band"]
        adv_fit = 1.0 - np.abs(diff_norm - adv)
        budget_vec = budget_vectors.get(band, default_budget)
        score = w["adventure_fit"] * adv_fit + w["budget_fit"] * budget_vec + w["popularity"] * pop
        ranked = list(route_ids[np.argsort(-score)][:10])

        rel_set = relevant[user]
        p5.append(precision_at_k(ranked, rel_set, 5))
        n5.append(ndcg_at_k(ranked, rel_set, 5))
        # Hit-rate@10: did at least one truly-relevant route make the top 10?
        hr10.append(1.0 if rel_set & set(ranked) else 0.0)
        base_hr10.append(1.0 if rel_set & base_top10 else 0.0)

    return {
        "precision_at_5": float(np.mean(p5)),
        "ndcg_at_5": float(np.mean(n5)),
        "hit_rate_at_10": float(np.mean(hr10)),
        "popularity_baseline_hit_rate_at_10": float(np.mean(base_hr10)),
        "lift_over_popularity": round(float(np.mean(hr10)) / max(float(np.mean(base_hr10)), 1e-9), 3),
        "n_eval_users": len(eval_users),
    }


def train() -> dict:
    routes = load_routes()
    interactions = load_interactions()
    interactions["year"] = pd.to_datetime(interactions["interaction_date"]).dt.year
    train_inter = interactions[interactions["year"] <= 2023]
    test_inter = interactions[interactions["year"] == 2024]

    profile = build_route_profile(routes, train_inter)
    metrics = _evaluate(profile, train_inter, test_inter)

    artifact = {"routes": profile[ARTIFACT_COLS].to_dict("records"), "weights": DEFAULT_WEIGHTS}
    notes = (
        "Content-based + popularity recommender. Popularity from train<=2023 only. "
        f"Offline eval on 2024 positive feedback over {metrics.get('n_eval_users', 0)} users."
    )
    card = save_model(
        name="route_recommender",
        model=artifact,
        metrics=metrics,
        params={"weights": DEFAULT_WEIGHTS},
        n_train=len(train_inter),
        notes=notes,
    )
    logger.info("recommender trained: %s", metrics)
    return {"card": card.version, "metrics": metrics}


if __name__ == "__main__":  # pragma: no cover
    logging.basicConfig(level=logging.INFO)
    import json

    print(json.dumps(train()["metrics"], indent=2))
