from __future__ import annotations

from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver

from src.common.events import Channels, publish_event
from .models import BookingSession


@receiver(post_save, sender=BookingSession)
def booking_status_changed(sender: type[BookingSession], instance: BookingSession, created: bool, **kwargs: Any) -> None:
    """Publish booking lifecycle events for realtime services.

    When a booking becomes ACTIVE, the realtime engine will notify participants.
    """
    event = 'booking.created' if created else f'booking.status.{instance.status.lower()}'
    payload = {
        'event': event,
        'booking_id': instance.pk,
        'booking_reference': instance.booking_reference,
        'status': instance.status,
        'tourist_id': instance.tourist_id,
        'assigned_guide_id': instance.assigned_guide_id,
        'timestamp': instance.updated_at.isoformat(),
    }
    publish_event(Channels.BOOKING, payload)
