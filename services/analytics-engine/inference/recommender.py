"""Online route recommendation (content-based + popularity, fully explainable)."""
from __future__ import annotations

from functools import lru_cache

import pandas as pd

from data.loader import load_interactions, load_routes
from features.recommender import DEFAULT_WEIGHTS, budget_fit, build_route_profile, season_fit
from registry import get_card, load_model


@lru_cache(maxsize=1)
def _profile() -> pd.DataFrame:
    """Use the trained artifact's profile if available, else build it live."""
    artifact = load_model("route_recommender")
    if artifact and "routes" in artifact:
        return pd.DataFrame(artifact["routes"])
    try:
        interactions = load_interactions()
    except FileNotFoundError:
        interactions = None
    return build_route_profile(load_routes(), interactions)


def _weights() -> dict[str, float]:
    artifact = load_model("route_recommender")
    if artifact and "weights" in artifact:
        return artifact["weights"]
    return DEFAULT_WEIGHTS


def recommend(*, tourist: dict, season: str | None = None, top_k: int = 5) -> dict:
    profile = _profile()
    weights = _weights()
    adventure = float(tourist.get("pref_adventure_score", 0.5))
    budget_band = tourist.get("budget_band")

    items = []
    for row in profile.itertuples(index=False):
        components = {
            "adventure_fit": round(1.0 - abs(row.difficulty_norm - adventure), 4),
            "season_fit": round(season_fit(row.best_seasons, season), 4),
            "budget_fit": round(budget_fit(row.estimated_cost_usd, budget_band), 4),
            "popularity": round(float(getattr(row, "popularity", 0.0)), 4),
        }
        score = sum(weights[k] * components[k] for k in weights)
        items.append(
            {
                "route_id": row.route_id,
                "route_name": row.route_name,
                "region": row.region,
                "difficulty": row.difficulty,
                "score": round(score, 4),
                "components": components,
            }
        )

    items.sort(key=lambda x: x["score"], reverse=True)
    card = get_card("route_recommender")
    return {"model_version": card.version if card else "content-heuristic", "items": items[:top_k]}
