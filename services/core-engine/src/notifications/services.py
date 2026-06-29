"""Helpers other apps use to raise notifications.

``create_notification`` writes the row (a ``post_save`` signal mirrors it to the
realtime engine). ``notify_async`` enqueues the same via Celery for hot paths.
"""
from __future__ import annotations

from typing import Any

from .models import Notification


def create_notification(
    *, recipient_id: int, kind: str, title: str, body: str = "", data: dict[str, Any] | None = None
) -> Notification:
    return Notification.objects.create(
        recipient_id=recipient_id, kind=kind, title=title, body=body, data=data
    )


def notify_async(*, recipient_id: int, kind: str, title: str, body: str = "", data: dict[str, Any] | None = None) -> None:
    from .tasks import send_notification

    send_notification.delay(recipient_id=recipient_id, kind=kind, title=title, body=body, data=data)
