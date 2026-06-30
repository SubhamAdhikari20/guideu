from __future__ import annotations

from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver

from src.common.events import Channels, publish_event
from .models import TrekkingPermit


@receiver(post_save, sender=TrekkingPermit)
def trekking_permit_status_changed(sender: type[TrekkingPermit], instance: TrekkingPermit, created: bool, **kwargs: Any) -> None:
    event = 'permit.created' if created else f'permit.status.{instance.status.lower()}'
    payload = {
        'event': event,
        'permit_id': instance.pk,
        'applicant_id': instance.applicant_id,
        'permit_type': instance.permit_type,
        'status': instance.status,
        'timestamp': instance.updated_at.isoformat(),
    }
    publish_event(Channels.PERMIT, payload)
