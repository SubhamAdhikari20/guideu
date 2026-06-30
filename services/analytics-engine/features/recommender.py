"""Feature engineering for the route recommender.

Builds an interpretable item profile for every route plus a popularity prior
from the interaction log. Scoring (in ``inference/recommender.py``) combines
these with the requesting tourist's survey scores into explainable component
terms — no opaque embedding, in line with the traceability requirement.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

# Component weights for the blended score (sum to 1). Shared by training (eval)
# and inference, and stored with the artifact so they are versioned.
DEFAULT_WEIGHTS = {"adventure_fit": 0.45, "season_fit": 0.2, "budget_fit": 0.2, "popularity": 0.15}

# Rough USD budget midpoints per band — used for the budget-fit term.
BUDGET_USD = {"Budget": 800, "Mid-range": 1500, "Comfort": 2500, "Luxury": 4000}

# Map a query season to the tokens the dataset uses in `best_seasons`.
SEASON_TOKENS = {
    "Spring": ["Spring", "All-year"],
    "Summer": ["Summer", "All-year"],
    "Monsoon": ["Summer", "All-year"],
    "Autumn": ["Autumn", "All-year"],
    "Winter": ["Winter", "All-year"],
}


def build_route_profile(routes: pd.DataFrame, interactions: pd.DataFrame | None = None) -> pd.DataFrame:
    """Return one row per route with normalised features + popularity prior."""
    profile = routes.copy()
    # Difficulty normalised to [0,1] aligns with a tourist's adventure score.
    profile["difficulty_norm"] = (profile["difficulty_level"].astype(float) - 1.0) / 3.0
    profile["difficulty_norm"] = profile["difficulty_norm"].clip(0, 1)

    if interactions is not None and not interactions.empty:
        route_inter = interactions[interactions["item_type"] == "Route"]
        pop = route_inter.groupby("item_id").size().rename("interaction_count")
        profile = profile.merge(pop, left_on="route_id", right_index=True, how="left")
    if "interaction_count" not in profile:
        profile["interaction_count"] = 0.0
    profile["interaction_count"] = profile["interaction_count"].fillna(0.0)

    max_pop = profile["interaction_count"].max()
    profile["popularity"] = profile["interaction_count"] / max_pop if max_pop else 0.0
    return profile


def season_fit(best_seasons: str, season: str | None) -> float:
    if not season:
        return 1.0
    tokens = SEASON_TOKENS.get(season.title(), [season])
    text = str(best_seasons or "")
    return 1.0 if any(tok in text for tok in tokens) else 0.3


def budget_fit(estimated_cost_usd: float, budget_band: str | None) -> float:
    if not budget_band or budget_band not in BUDGET_USD:
        return 0.7
    target = BUDGET_USD[budget_band]
    return float(np.exp(-abs(float(estimated_cost_usd) - target) / target))
