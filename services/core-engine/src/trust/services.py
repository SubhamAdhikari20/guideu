"""Anti-scam price-check service.

Resolves a fair benchmark for a (service, region, season), computes the
overcharge ratio, and asks the analytics-engine for a calibrated scam
probability. If the ML service is unavailable it degrades gracefully to the
deterministic benchmark rule, so the feature always works.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass

from src.catalog.models import PricingBenchmark
from src.common.services import get_analytics_client

from .models import classify_severity


@dataclass
class PriceCheckResult:
    service_type: str
    region: str | None
    season: str | None
    quoted_price_npr: int
    benchmark_price_npr: int | None
    overcharge_ratio: float | None
    is_likely_scam: bool
    severity: str | None
    scam_probability: float | None
    source: str  # "ml" | "benchmark" | "unknown"
    explanation: list[str]

    def as_dict(self) -> dict:
        return asdict(self)


# Flag when the quote exceeds the fair benchmark by >25% (dataset convention).
SCAM_RATIO_THRESHOLD = 1.25


def check_price(*, service_type: str, region: str | None, season: str | None, quoted_price_npr: int) -> PriceCheckResult:
    benchmark = PricingBenchmark.fair_price_for(service_type=service_type, region_name=region, season=season)
    explanation: list[str] = []

    if benchmark is None:
        explanation.append("No fair-price benchmark exists for this service yet.")
        return PriceCheckResult(
            service_type=service_type, region=region, season=season, quoted_price_npr=quoted_price_npr,
            benchmark_price_npr=None, overcharge_ratio=None, is_likely_scam=False, severity=None,
            scam_probability=None, source="unknown", explanation=explanation,
        )

    fair = benchmark["fair_price_npr"]
    ratio = round(quoted_price_npr / fair, 3) if fair else None
    severity = classify_severity(ratio) if ratio is not None else None
    explanation.append(f"Fair benchmark is ~{fair} NPR (n={benchmark['sample_size']} samples).")
    if ratio is not None:
        explanation.append(f"Quoted price is {ratio}x the fair benchmark.")
    if quoted_price_npr < benchmark["min_fair_npr"]:
        explanation.append("Quote is below the fair range — possible below-fair-wage offer.")

    # Try the ML service for a calibrated probability; fall back to the rule.
    ml = get_analytics_client().score_scam(
        service_type=service_type, region=region or "", season=season or "", quoted_price_npr=quoted_price_npr
    )
    if ml and "scam_probability" in ml:
        explanation.append("Scored by the anti-scam model.")
        return PriceCheckResult(
            service_type=service_type, region=region, season=season, quoted_price_npr=quoted_price_npr,
            benchmark_price_npr=fair, overcharge_ratio=ratio, is_likely_scam=bool(ml.get("is_likely_scam")),
            severity=ml.get("severity", severity), scam_probability=ml.get("scam_probability"),
            source="ml", explanation=explanation,
        )

    return PriceCheckResult(
        service_type=service_type, region=region, season=season, quoted_price_npr=quoted_price_npr,
        benchmark_price_npr=fair, overcharge_ratio=ratio,
        is_likely_scam=bool(ratio and ratio > SCAM_RATIO_THRESHOLD), severity=severity,
        scam_probability=None, source="benchmark", explanation=explanation,
    )
