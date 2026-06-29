"""User event tracking and ML feature logging.

This is the in-app analogue of the dataset's ``recommendation_interactions``
table: a stream of view/click/search/book events that feeds funnel analytics and
the recommender's implicit-feedback signal. Events are pseudonymous (a user id,
never raw PII) to honour the privacy stance in ``docs/ethics-and-fairness.md``.
"""
from __future__ import annotations

from django.conf import settings
from django.db import models
from django.db.models import Count

from src.common.models import TimeStampedModel


class EventType(models.TextChoices):
    VIEW = "VIEW", "View"
    CLICK = "CLICK", "Click"
    SEARCH = "SEARCH", "Search"
    WISHLIST = "WISHLIST", "Wishlist"
    BOOK = "BOOK", "Book"
    RATE = "RATE", "Rate"
    SHARE = "SHARE", "Share"
    COMPLETE = "COMPLETE", "Complete"
    SCAM_CHECK = "SCAM_CHECK", "Scam check"


class UserEventQuerySet(models.QuerySet):
    def funnel(self) -> dict[str, int]:
        """Counts per event type — the basis for funnel/conversion dashboards."""
        rows = self.values("event_type").annotate(n=Count("id"))
        return {row["event_type"]: row["n"] for row in rows}


class UserEvent(TimeStampedModel):
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name="events"
    )
    event_type = models.CharField(max_length=16, choices=EventType.choices, db_index=True)
    item_type = models.CharField(max_length=16, blank=True, help_text="Route / Guide / Event / ...")
    item_id = models.CharField(max_length=64, blank=True, db_index=True)
    session_id = models.CharField(max_length=64, blank=True, db_index=True)
    source = models.CharField(max_length=64, blank=True, help_text="In-app surface, e.g. Recommendation Feed")
    device = models.CharField(max_length=16, blank=True)
    metadata = models.JSONField(null=True, blank=True)

    objects = UserEventQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["event_type", "-created_at"]),
            models.Index(fields=["item_type", "item_id"]),
            models.Index(fields=["actor", "-created_at"]),
        ]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.actor_id or 'anon'} {self.event_type} {self.item_type}:{self.item_id}"
