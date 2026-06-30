"""Evaluation metrics for the GuideU models."""
from __future__ import annotations

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)


def classification_metrics(y_true, y_prob, threshold: float = 0.5) -> dict[str, float]:
    """Standard binary-classification metrics for the scam model."""
    y_true = np.asarray(y_true)
    y_prob = np.asarray(y_prob)
    y_pred = (y_prob >= threshold).astype(int)
    metrics = {
        "accuracy": accuracy_score(y_true, y_pred),
        "precision": precision_score(y_true, y_pred, zero_division=0),
        "recall": recall_score(y_true, y_pred, zero_division=0),
        "f1": f1_score(y_true, y_pred, zero_division=0),
    }
    # AUC metrics require both classes present.
    if len(np.unique(y_true)) > 1:
        metrics["roc_auc"] = roc_auc_score(y_true, y_prob)
        metrics["pr_auc"] = average_precision_score(y_true, y_prob)
    return metrics


def roc_auc_or_none(y_true, y_prob) -> float | None:
    """ROC-AUC, or None when only one class is present in the slice."""
    y_true = np.asarray(y_true)
    if len(np.unique(y_true)) < 2:
        return None
    return round(float(roc_auc_score(y_true, np.asarray(y_prob))), 4)


def precision_at_k(recommended_ids: list[str], relevant_ids: set[str], k: int) -> float:
    if k == 0:
        return 0.0
    top = recommended_ids[:k]
    hits = sum(1 for item in top if item in relevant_ids)
    return hits / k


def ndcg_at_k(recommended_ids: list[str], relevant_ids: set[str], k: int) -> float:
    top = recommended_ids[:k]
    dcg = sum(1.0 / np.log2(i + 2) for i, item in enumerate(top) if item in relevant_ids)
    ideal_hits = min(len(relevant_ids), k)
    idcg = sum(1.0 / np.log2(i + 2) for i in range(ideal_hits))
    return float(dcg / idcg) if idcg else 0.0
