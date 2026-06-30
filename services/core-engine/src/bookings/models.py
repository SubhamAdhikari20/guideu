from __future__ import annotations

from decimal import Decimal
from typing import Any

from django.core.exceptions import ValidationError
from django.db import models

from src.authentication.models import TimeStampedModel, User


class TourPackage(TimeStampedModel):
    """A tour package offering that tourists can book.

    This model is intended to be read-heavy and cached by the realtime
    services when needed.
    """

    title = models.CharField(max_length=255, help_text='Display title for the tour package')
    description = models.TextField(blank=True)
    base_price = models.DecimalField(max_digits=10, decimal_places=2, help_text='Base price in platform currency')
    duration_days = models.PositiveSmallIntegerField(default=1, help_text='Typical duration in days')
    capacity = models.PositiveSmallIntegerField(default=1, help_text='Max number of tourists allowed')
    is_active = models.BooleanField(default=True, db_index=True)

    class Meta:
        verbose_name = 'tour package'
        verbose_name_plural = 'tour packages'

    def __str__(self) -> str:  # pragma: no cover - trivial
        return self.title


class BookingSession(TimeStampedModel):
    """Represents a booking lifecycle for a tourist on a given `TourPackage`.

    Status lifecycle: PENDING -> CONFIRMED -> ACTIVE -> COMPLETED | CANCELLED
    """

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        ACTIVE = 'ACTIVE', 'Active'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    tourist = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='bookings', db_index=True)
    tour_package = models.ForeignKey('bookings.TourPackage', on_delete=models.PROTECT, related_name='bookings', db_index=True)
    # Optional link to a dataset-backed trekking route (additive, non-breaking).
    route = models.ForeignKey('catalog.TrekkingRoute', on_delete=models.PROTECT, null=True, blank=True, related_name='bookings', db_index=True)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING, db_index=True)
    assigned_guide = models.ForeignKey('authentication.User', on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_bookings', db_index=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    booking_reference = models.CharField(max_length=64, unique=True, db_index=True)
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'booking session'
        verbose_name_plural = 'booking sessions'
        indexes = [
            models.Index(fields=['status']),
            models.Index(fields=['tourist']),
            models.Index(fields=['assigned_guide']),
        ]

    def clean(self) -> None:
        if self.end_date <= self.start_date:
            raise ValidationError({'end_date': 'end_date must be after start_date'})
        if self.assigned_guide and self.assigned_guide.role != User.Roles.GUIDE:
            raise ValidationError({'assigned_guide': 'Assigned user must be a guide'})

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        super().save(*args, **kwargs)


class ItineraryItem(TimeStampedModel):
    booking = models.ForeignKey('bookings.BookingSession', on_delete=models.CASCADE, related_name='itinerary_items', db_index=True)
    day_index = models.PositiveIntegerField(help_text='Day number within the tour, starting from 1')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    location = models.JSONField(blank=True, null=True, help_text='Geo location or place metadata (GeoJSON)')
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'itinerary item'
        verbose_name_plural = 'itinerary items'
        ordering = ['booking', 'day_index']

    def __str__(self) -> str:  # pragma: no cover - trivial
        return f"{self.booking.booking_reference} - Day {self.day_index}: {self.title}"
