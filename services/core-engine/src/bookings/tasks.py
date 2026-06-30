"""Celery tasks for the bookings domain."""
from __future__ import annotations

from datetime import timedelta

from celery import shared_task
from django.utils import timezone


@shared_task(name="src.bookings.tasks.expire_stale_pending_bookings")
def expire_stale_pending_bookings(max_age_hours: int = 24) -> int:
    """Cancel bookings stuck in PENDING beyond ``max_age_hours``.

    Keeps inventory/availability honest. Scheduled hourly via Celery beat
    (see ``CELERY_BEAT_SCHEDULE``). Returns the number of bookings expired.
    """
    from .models import BookingSession

    cutoff = timezone.now() - timedelta(hours=max_age_hours)
    stale = BookingSession.objects.filter(status=BookingSession.Status.PENDING, created_at__lt=cutoff)
    count = 0
    for booking in stale.iterator():
        booking.status = BookingSession.Status.CANCELLED
        booking.save(update_fields=["status", "updated_at"])  # fires the realtime signal
        count += 1
    return count
