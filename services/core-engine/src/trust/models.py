"""Anti-scam: tourist overcharge reports and price-check logs.

Maps the dataset's ``scam_reports.csv`` concept into an app workflow. The
``overcharge_ratio = quoted / benchmark`` is the fair, explainable basis for a
flag; protected attributes (nationality) are deliberately *not* stored as model
features here — see ``docs/ethics-and-fairness.md``.
"""
from __future__ import annotations

from django.conf import settings
from django.db import models

from src.common.models import TimeStampedModel


class ScamSeverity(models.TextChoices):
    FAIR = "Fair", "Fair"
    MILD = "Mild Overcharge", "Mild Overcharge"
    MODERATE = "Moderate Overcharge", "Moderate Overcharge"
    SEVERE = "Severe Overcharge", "Severe Overcharge"
    LIKELY_SCAM = "Likely Scam", "Likely Scam"


def classify_severity(overcharge_ratio: float) -> str:
    """Deterministic severity banding (mirrors the dataset generator)."""
    if overcharge_ratio < 1.10:
        return ScamSeverity.FAIR
    if overcharge_ratio < 1.30:
        return ScamSeverity.MILD
    if overcharge_ratio < 1.70:
        return ScamSeverity.MODERATE
    if overcharge_ratio < 2.50:
        return ScamSeverity.SEVERE
    return ScamSeverity.LIKELY_SCAM


class ScamReport(TimeStampedModel):
    class Status(models.TextChoices):
        SUBMITTED = "SUBMITTED", "Submitted"
        VERIFIED = "VERIFIED", "Verified"
        DISMISSED = "DISMISSED", "Dismissed"

    reporter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="scam_reports")
    service_type = models.CharField(max_length=64, db_index=True)
    region = models.ForeignKey("catalog.Region", on_delete=models.PROTECT, related_name="scam_reports")
    season = models.CharField(max_length=32, blank=True)
    quoted_price_npr = models.PositiveIntegerField()
    benchmark_price_npr = models.PositiveIntegerField(help_text="Fair benchmark resolved at submission")
    overcharge_ratio = models.FloatField(db_index=True)
    scam_severity = models.CharField(max_length=24, choices=ScamSeverity.choices, db_index=True)
    was_flagged_by_app = models.BooleanField(default=False, db_index=True)
    ml_scam_probability = models.FloatField(null=True, blank=True, help_text="Score from the analytics-engine, if available")
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.SUBMITTED, db_index=True)
    verified_by_moderator = models.BooleanField(default=False)
    description = models.TextField(blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["service_type", "region"])]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.service_type} x{self.overcharge_ratio:.2f} ({self.scam_severity})"


class PriceCheck(TimeStampedModel):
    """A logged anti-scam price check (the user-facing 'is this fair?' tool)."""

    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="price_checks"
    )
    service_type = models.CharField(max_length=64, db_index=True)
    region = models.CharField(max_length=64, blank=True)
    season = models.CharField(max_length=32, blank=True)
    quoted_price_npr = models.PositiveIntegerField()
    benchmark_price_npr = models.PositiveIntegerField(null=True, blank=True)
    overcharge_ratio = models.FloatField(null=True, blank=True)
    is_likely_scam = models.BooleanField(default=False)
    source = models.CharField(max_length=16, default="benchmark", help_text="benchmark | ml")

    class Meta:
        ordering = ["-created_at"]
