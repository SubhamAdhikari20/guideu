"""Append-only audit trail for sensitive, state-changing API actions."""
from __future__ import annotations

from django.conf import settings
from django.db import models

from src.common.models import TimeStampedModel


class AuditLog(TimeStampedModel):
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="audit_logs",
    )
    method = models.CharField(max_length=8)
    path = models.CharField(max_length=512)
    status_code = models.PositiveSmallIntegerField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.CharField(max_length=512, blank=True)
    metadata = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["actor", "-created_at"]),
            models.Index(fields=["path"]),
        ]

    def __str__(self) -> str:  # pragma: no cover - trivial
        who = self.actor_id or "anon"
        return f"{who} {self.method} {self.path} -> {self.status_code}"
