"""Gamification — badges and points (maps the dataset's ``gamification_log``).

Badges encourage safe, fair, culturally-engaged travel (e.g. *Scam Spotter* for
reporting a verified overcharge, *Fair Pay Advocate* for paying within
benchmark) — reinforcing the platform's anti-scam, pro-local-worker values.
"""
from __future__ import annotations

from django.conf import settings
from django.db import models

from src.common.models import TimeStampedModel


class BadgeCategory(models.TextChoices):
    CULTURAL = "Cultural", "Cultural"
    ADVENTURE = "Adventure", "Adventure"
    EXPLORER = "Explorer", "Explorer"
    SAFETY = "Safety", "Safety"


class Badge(TimeStampedModel):
    name = models.CharField(max_length=64, unique=True)
    category = models.CharField(max_length=16, choices=BadgeCategory.choices, db_index=True)
    points = models.PositiveIntegerField(default=0)
    trigger_event = models.CharField(max_length=128, blank=True, help_text="What earns this badge")
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["category", "name"]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.name


class BadgeAward(TimeStampedModel):
    """A badge earned by a user (one award per badge per user)."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="badge_awards")
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE, related_name="awards")
    points_awarded = models.PositiveIntegerField(default=0)
    trigger_event = models.CharField(max_length=128, blank=True)

    class Meta:
        ordering = ["-created_at"]
        constraints = [models.UniqueConstraint(fields=["user", "badge"], name="uniq_badge_per_user")]
        indexes = [models.Index(fields=["user", "-created_at"])]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.user_id} earned {self.badge_id}"

    def save(self, *args, **kwargs):
        if not self.points_awarded and self.badge_id:
            self.points_awarded = self.badge.points
        super().save(*args, **kwargs)
