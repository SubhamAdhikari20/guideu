"""Post-hoc fairness audit for the anti-scam classifier.

The dataset deliberately simulates tourist-price discrimination by nationality.
Because we *exclude* protected attributes from the features, the model should not
reproduce that bias. This audit verifies it: it reports the model's flag-rate and
ROC-AUC per continent and the disparity between groups. A large flag-rate
disparity is a red flag that the model has found a proxy for nationality.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

from .metrics import roc_auc_or_none


def fairness_report(df: pd.DataFrame, y_true, y_prob, group_col: str = "continent", threshold: float = 0.5) -> dict:
    """Per-group flag-rate / AUC and the overall disparity."""
    audit = pd.DataFrame(
        {"group": df[group_col].to_numpy(), "y_true": np.asarray(y_true), "y_prob": np.asarray(y_prob)}
    )
    audit["y_pred"] = (audit["y_prob"] >= threshold).astype(int)

    groups: dict[str, dict[str, float]] = {}
    for name, chunk in audit.groupby("group"):
        groups[str(name)] = {
            "n": int(len(chunk)),
            "flag_rate": round(float(chunk["y_pred"].mean()), 4),
            "actual_rate": round(float(chunk["y_true"].mean()), 4),
            "roc_auc": roc_auc_or_none(chunk["y_true"], chunk["y_prob"]),
        }

    flag_rates = [g["flag_rate"] for g in groups.values()]
    disparity = round(max(flag_rates) - min(flag_rates), 4) if flag_rates else 0.0
    return {
        "group_col": group_col,
        "groups": groups,
        "flag_rate_disparity": disparity,
        "passes": disparity < 0.15,  # heuristic gate documented in ethics-and-fairness.md
    }
