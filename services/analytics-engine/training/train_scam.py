"""Train the anti-scam classifier on ``scam_reports.csv``.

Baseline-first (logistic regression over one-hot service/region + scaled price).
Honest temporal split (train 2021-2023, test 2024), reports classification
metrics and a fairness audit by continent, then registers the model.
"""
from __future__ import annotations

import logging

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from data.loader import load_scam_reports, load_tourists
from evaluation.fairness import fairness_report
from evaluation.metrics import classification_metrics
from features.scam import CATEGORICAL_FEATURES, NUMERIC_FEATURES, build_scam_frame
from registry import save_model

logger = logging.getLogger("guideu.ml.train.scam")


def _build_pipeline() -> Pipeline:
    pre = ColumnTransformer(
        transformers=[
            ("cat", OneHotEncoder(handle_unknown="ignore"), CATEGORICAL_FEATURES),
            ("num", StandardScaler(), NUMERIC_FEATURES),
        ]
    )
    return Pipeline(
        steps=[
            ("features", pre),
            ("clf", LogisticRegression(max_iter=1000, class_weight="balanced")),
        ]
    )


def train() -> dict:
    df = load_scam_reports()
    # Join continent for the fairness audit only — NOT used as a feature.
    tourists = load_tourists()[["tourist_id", "continent"]]
    df = df.merge(tourists, on="tourist_id", how="left")
    df["year"] = pd.to_datetime(df["reported_date"]).dt.year

    train_df = df[df["year"] <= 2023]
    test_df = df[df["year"] == 2024]
    if test_df.empty:  # fallback if the split leaves no test rows
        from sklearn.model_selection import train_test_split

        train_df, test_df = train_test_split(df, test_size=0.2, random_state=42, stratify=df["was_flagged_by_app"])

    X_train, y_train = build_scam_frame(train_df)
    X_test, y_test = build_scam_frame(test_df)

    pipeline = _build_pipeline()
    pipeline.fit(X_train, y_train)

    y_prob = pipeline.predict_proba(X_test)[:, 1]
    metrics = classification_metrics(y_test, y_prob)
    fairness = fairness_report(test_df, y_test, y_prob, group_col="continent")
    metrics["fairness_flag_rate_disparity"] = fairness["flag_rate_disparity"]

    notes = (
        f"Logistic baseline. Temporal split train<=2023 (n={len(train_df)}), test=2024 (n={len(test_df)}). "
        f"Fairness gate {'PASS' if fairness['passes'] else 'REVIEW'} "
        f"(continent flag-rate disparity={fairness['flag_rate_disparity']}). "
        "Protected attributes excluded from features."
    )
    card = save_model(
        name="scam_classifier",
        model=pipeline,
        metrics=metrics,
        params={"model": "LogisticRegression", "class_weight": "balanced", "features": NUMERIC_FEATURES + CATEGORICAL_FEATURES},
        n_train=len(train_df),
        notes=notes,
    )
    logger.info("scam model trained: %s", metrics)
    return {"card": card.version, "metrics": metrics, "fairness": fairness}


if __name__ == "__main__":  # pragma: no cover
    logging.basicConfig(level=logging.INFO)
    import json

    print(json.dumps(train()["metrics"], indent=2))
