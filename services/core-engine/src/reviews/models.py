"""User reviews for guides and routes, with moderation and rating aggregation."""
from __future__ import annotations

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Avg, Count

from src.common.models import TimeStampedModel


class ReviewQuerySet(models.QuerySet):
    def approved(self) -> "ReviewQuerySet":
        return self.filter(status=Review.Status.APPROVED)

    def summary(self) -> dict:
        agg = self.approved().aggregate(average=Avg("rating"), count=Count("id"))
        return {"average_rating": round(agg["average"] or 0, 2), "review_count": agg["count"]}


class Review(TimeStampedModel):
    """A rating + comment a tourist leaves for a guide or a route.

    Exactly one of ``guide`` / ``route`` is set (enforced by a DB constraint).
    New reviews start ``PENDING`` and become visible only once moderated.
    """

    class Status(models.TextChoices):
        PENDING = "PENDING", "Pending moderation"
        APPROVED = "APPROVED", "Approved"
        REJECTED = "REJECTED", "Rejected"

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="reviews")
    guide = models.ForeignKey("catalog.GuideRegistry", on_delete=models.CASCADE, null=True, blank=True, related_name="reviews")
    route = models.ForeignKey("catalog.TrekkingRoute", on_delete=models.CASCADE, null=True, blank=True, related_name="reviews")
    booking = models.ForeignKey("bookings.BookingSession", on_delete=models.SET_NULL, null=True, blank=True, related_name="reviews")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], db_index=True)
    title = models.CharField(max_length=140, blank=True)
    comment = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.PENDING, db_index=True)
    is_flagged = models.BooleanField(default=False, db_index=True)
    helpful_count = models.PositiveIntegerField(default=0)

    objects = ReviewQuerySet.as_manager()

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.CheckConstraint(
                name="review_exactly_one_target",
                condition=(
                    models.Q(guide__isnull=False, route__isnull=True)
                    | models.Q(guide__isnull=True, route__isnull=False)
                ),
            ),
            models.UniqueConstraint(
                fields=["author", "guide"], condition=models.Q(guide__isnull=False), name="uniq_review_author_guide"
            ),
            models.UniqueConstraint(
                fields=["author", "route"], condition=models.Q(route__isnull=False), name="uniq_review_author_route"
            ),
        ]

    def __str__(self) -> str:  # pragma: no cover - trivial
        target = self.guide_id and f"guide:{self.guide_id}" or f"route:{self.route_id}"
        return f"{self.author_id} -> {target} ({self.rating}★)"

    @property
    def target_kind(self) -> str:
        return "guide" if self.guide_id else "route"
