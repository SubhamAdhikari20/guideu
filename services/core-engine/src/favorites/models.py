"""Wishlist (saved routes/guides) and recently-viewed history."""
from __future__ import annotations

from django.conf import settings
from django.db import models

from src.common.models import TimeStampedModel


class Favorite(TimeStampedModel):
    """A saved route or guide. Exactly one target is set."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    route = models.ForeignKey("catalog.TrekkingRoute", on_delete=models.CASCADE, null=True, blank=True, related_name="favorited_by")
    guide = models.ForeignKey("catalog.GuideRegistry", on_delete=models.CASCADE, null=True, blank=True, related_name="favorited_by")

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                name="favorite_exactly_one_target",
                condition=(
                    models.Q(route__isnull=False, guide__isnull=True)
                    | models.Q(route__isnull=True, guide__isnull=False)
                ),
            ),
            models.UniqueConstraint(fields=["user", "route"], condition=models.Q(route__isnull=False), name="uniq_fav_user_route"),
            models.UniqueConstraint(fields=["user", "guide"], condition=models.Q(guide__isnull=False), name="uniq_fav_user_guide"),
        ]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.user_id} ♥ {'route:' + str(self.route_id) if self.route_id else 'guide:' + str(self.guide_id)}"


class RecentlyViewed(TimeStampedModel):
    """Lightweight recently-viewed log (used as an implicit recommender signal)."""

    class ItemType(models.TextChoices):
        ROUTE = "Route", "Route"
        GUIDE = "Guide", "Guide"
        EVENT = "Event", "Event"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="recently_viewed")
    item_type = models.CharField(max_length=8, choices=ItemType.choices)
    item_id = models.CharField(max_length=32, help_text="Dataset external_id or local id")

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["user", "-created_at"])]
