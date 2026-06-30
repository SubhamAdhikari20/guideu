"""Feature engineering for the anti-scam classifier.

Design choices that matter for the thesis:

* **Protected attributes are excluded.** ``nationality`` / ``continent`` are
  never features — the dataset encodes a real-world nationality price-bias and we
  refuse to let the model launder that into automated discrimination.
* **The trivially-leaking columns are excluded.** ``was_flagged_by_app`` is, in
  the generator, a deterministic function of ``overcharge_ratio`` (and hence of
  ``benchmark_price_npr``). Feeding those back would yield a meaningless ~1.0
  AUC. Instead the model predicts the flag from ``service_type``, ``region`` and
  the raw ``quoted_price_npr`` — i.e. it learns typical price bands per service
  and region and detects anomalies, which generalises to quotes with no exact
  benchmark.
"""
from __future__ import annotations

import numpy as np
import pandas as pd

NUMERIC_FEATURES = ["quoted_price_npr", "log_quoted_price"]
CATEGORICAL_FEATURES = ["service_type", "region"]
FEATURES = NUMERIC_FEATURES + CATEGORICAL_FEATURES
TARGET = "was_flagged_by_app"
PROTECTED = ["nationality", "continent"]  # documented, never used as features


def build_scam_frame(df: pd.DataFrame) -> tuple[pd.DataFrame, pd.Series]:
    """Return (X, y) for training/evaluation."""
    frame = df.copy()
    frame["log_quoted_price"] = np.log1p(frame["quoted_price_npr"].astype(float))
    X = frame[FEATURES]
    y = frame[TARGET].astype(int)
    return X, y


def build_inference_row(*, service_type: str, region: str, quoted_price_npr: float) -> pd.DataFrame:
    """Single-row feature frame for online scoring."""
    return pd.DataFrame(
        [
            {
                "quoted_price_npr": float(quoted_price_npr),
                "log_quoted_price": float(np.log1p(quoted_price_npr)),
                "service_type": service_type,
                "region": region,
            }
        ]
    )
