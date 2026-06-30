"""In-app notifications with read/unread state; mirrored to the realtime engine."""
from __future__ import annotations

from django.conf import settings
from django.db import models
from django.utils import timezone

from src.common.models import TimeStampedModel


class Notification(TimeStampedModel):
    class Kind(models.TextChoices):
        BOOKING = "BOOKING", "Booking"
        PAYMENT = "PAYMENT", "Payment"
        PERMIT = "PERMIT", "Permit"
        REVIEW = "REVIEW", "Review"
        SCAM = "SCAM", "Scam alert"
        GAMIFICATION = "GAMIFICATION", "Gamification"
        SYSTEM = "SYSTEM", "System"

    recipient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    kind = models.CharField(max_length=16, choices=Kind.choices, default=Kind.SYSTEM, db_index=True)
    title = models.CharField(max_length=180)
    body = models.TextField(blank=True)
    data = models.JSONField(null=True, blank=True, help_text="Structured payload for deep-linking in the apps")
    is_read = models.BooleanField(default=False, db_index=True)
    read_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["recipient", "is_read", "-created_at"])]

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"[{self.kind}] {self.title} -> {self.recipient_id}"

    def mark_read(self) -> None:
        if not self.is_read:
            self.is_read = True
            self.read_at = timezone.now()
            self.save(update_fields=["is_read", "read_at", "updated_at"])
