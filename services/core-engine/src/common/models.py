"""Shared abstract base models for the GuideU core engine.

These live in ``common`` so every domain app depends on a single, neutral
foundation rather than importing base classes from ``authentication`` (which
created an implicit dependency from, e.g., ``payments`` onto the accounts app).
``authentication.models`` re-exports :class:`TimeStampedModel` for backward
compatibility.
"""
from __future__ import annotations

import uuid
from typing import Any

from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """Abstract base model with creation and update timestamps."""

    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class UUIDModel(models.Model):
    """Abstract base that uses a non-sequential UUID primary key.

    Used for resources that are exposed in URLs/QR codes where a sequential
    integer id would leak volume or enable enumeration (e.g. bookings).
    """

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class SoftDeleteQuerySet(models.QuerySet):
    """QuerySet that supports soft deletion."""

    def delete(self) -> tuple[int, dict[str, int]]:  # type: ignore[override]
        return super().update(is_deleted=True, deleted_at=timezone.now()), {}

    def hard_delete(self) -> tuple[int, dict[str, int]]:
        return super().delete()

    def alive(self) -> "SoftDeleteQuerySet":
        return self.filter(is_deleted=False)


class SoftDeleteManager(models.Manager):
    """Default manager that hides soft-deleted rows."""

    def get_queryset(self) -> SoftDeleteQuerySet:
        return SoftDeleteQuerySet(self.model, using=self._db).filter(is_deleted=False)


class SoftDeleteModel(TimeStampedModel):
    """Abstract base providing reversible deletion.

    ``objects`` excludes deleted rows; ``all_objects`` includes them so admins
    and audit flows can still see history.
    """

    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = SoftDeleteManager()
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def delete(self, using: Any = None, keep_parents: bool = False) -> tuple[int, dict[str, int]]:  # type: ignore[override]
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(using=using, update_fields=["is_deleted", "deleted_at", "updated_at"])
        return 1, {}

    def hard_delete(self, using: Any = None, keep_parents: bool = False) -> tuple[int, dict[str, int]]:
        return super().delete(using=using, keep_parents=keep_parents)
