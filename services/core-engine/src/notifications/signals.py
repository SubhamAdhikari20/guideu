from __future__ import annotations

from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver

from src.common.events import Channels, publish_event

from .models import Notification


@receiver(post_save, sender=Notification)
def mirror_notification_to_realtime(sender: type[Notification], instance: Notification, created: bool, **kwargs: Any) -> None:
    """Push newly created notifications to the realtime engine for live delivery."""
    if not created:
        return
    publish_event(
        Channels.NOTIFICATION,
        {
            "event": "notification.created",
            "notification_id": instance.pk,
            "user_id": instance.recipient_id,
            "kind": instance.kind,
            "title": instance.title,
            "body": instance.body,
            "timestamp": instance.created_at.isoformat(),
        },
    )
