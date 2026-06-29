"""Celery tasks for asynchronous notification delivery."""
from __future__ import annotations

from typing import Any

from celery import shared_task


@shared_task(name="src.notifications.tasks.send_notification")
def send_notification(*, recipient_id: int, kind: str, title: str, body: str = "", data: dict[str, Any] | None = None) -> int:
    """Create a notification off the request path. Returns the new id."""
    from .services import create_notification

    notification = create_notification(recipient_id=recipient_id, kind=kind, title=title, body=body, data=data)
    return notification.pk
