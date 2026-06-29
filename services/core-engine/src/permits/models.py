from __future__ import annotations

from typing import Any

from django.core.exceptions import ValidationError
from django.db import models

from src.authentication.models import TimeStampedModel


class TrekkingPermit(TimeStampedModel):
    """Model representing trekking permits (TIMS, National Park permits).

    Documents are stored as metadata in `documents` JSON for simplicity. In a
    production system, use a protected file storage backed by S3 and a file model.
    """

    class PermitType(models.TextChoices):
        TIMS = 'TIMS', 'TIMS'
        ANNAPURNA = 'ANNAPURNA', 'Annapurna National Park'
        EVEREST = 'EVEREST', 'Everest National Park'
        LANGTANG = 'LANGTANG', 'Langtang National Park'

    class Status(models.TextChoices):
        APPLIED = 'APPLIED', 'Applied'
        VERIFIED = 'VERIFIED', 'Verified'
        REJECTED = 'REJECTED', 'Rejected'

    applicant = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='permits', db_index=True)
    permit_type = models.CharField(max_length=32, choices=PermitType.choices, db_index=True)
    applied_date = models.DateField()
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.APPLIED, db_index=True)
    documents = models.JSONField(blank=True, null=True, help_text='Uploaded document metadata (paths, checksums, types)')
    route_bounds = models.JSONField(blank=True, null=True, help_text='GeoJSON bounding box or path for the trek')
    admin_notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'trekking permit'
        verbose_name_plural = 'trekking permits'

    def clean(self) -> None:
        if not self.documents:
            raise ValidationError({'documents': 'At least one verification document must be provided.'})

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        super().save(*args, **kwargs)
