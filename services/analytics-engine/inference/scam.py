"""Online anti-scam scoring.

Serves the trained classifier when present, otherwise a calibrated benchmark
heuristic, so the endpoint always returns an explainable verdict.
"""
from __future__ import annotations

import math

from features.scam import build_inference_row
from inference import pricing
from registry import get_card, load_model

SCAM_RATIO_THRESHOLD = 1.25


def classify_severity(ratio: float) -> str:
    if ratio < 1.10:
        return "Fair"
    if ratio < 1.30:
        return "Mild Overcharge"
    if ratio < 1.70:
        return "Moderate Overcharge"
    if ratio < 2.50:
        return "Severe Overcharge"
    return "Likely Scam"


def _heuristic_probability(ratio: float) -> float:
    """Smooth logistic around the 1.25 flag threshold (fallback when untrained)."""
    return round(1.0 / (1.0 + math.exp(-6.0 * (ratio - SCAM_RATIO_THRESHOLD))), 4)


def score(*, service_type: str, region: str | None, season: str | None, quoted_price_npr: float) -> dict:
    benchmark = pricing.fair_price(service_type, region or None, season or None)
    explanation: list[str] = []

    ratio = None
    if benchmark:
        fair = benchmark["fair_price_npr"]
        ratio = round(quoted_price_npr / fair, 3) if fair else None
        explanation.append(f"Fair benchmark ~{fair} NPR ({benchmark['granularity']}).")
        if ratio is not None:
            explanation.append(f"Quote is {ratio}x the benchmark.")
    else:
        explanation.append("No benchmark available for this service.")

    model = load_model("scam_classifier")
    if model is not None:
        row = build_inference_row(service_type=service_type, region=region or "", quoted_price_npr=quoted_price_npr)
        probability = float(model.predict_proba(row)[0, 1])
        card = get_card("scam_classifier")
        model_version = card.version if card else "scam_classifier"
        explanation.append("Scored by the trained anti-scam classifier.")
    elif ratio is not None:
        probability = _heuristic_probability(ratio)
        model_version = "heuristic-benchmark"
        explanation.append("Scored by the benchmark heuristic (model not trained yet).")
    else:
        probability = 0.0
        model_version = "unknown"

    severity = classify_severity(ratio) if ratio is not None else None
    is_likely_scam = probability >= 0.5 or bool(ratio and ratio > SCAM_RATIO_THRESHOLD)

    return {
        "scam_probability": round(probability, 4),
        "is_likely_scam": is_likely_scam,
        "severity": severity,
        "benchmark_price_npr": benchmark["fair_price_npr"] if benchmark else None,
        "overcharge_ratio": ratio,
        "model_version": model_version,
        "explanation": explanation,
    }
