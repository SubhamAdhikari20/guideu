from __future__ import annotations

from typing import Any

from django.db.models.signals import post_save
from django.dispatch import receiver

from src.common.events import Channels, publish_event
from .models import PaymentTransaction


@receiver(post_save, sender=PaymentTransaction)
def payment_transaction_changed(sender: type[PaymentTransaction], instance: PaymentTransaction, created: bool, **kwargs: Any) -> None:
    event = 'payment.created' if created else f'payment.status.{instance.status.lower()}'
    payload = {
        'event': event,
        'payment_id': instance.pk,
        'user_id': instance.user_id,
        'booking_id': instance.booking_id,
        'status': instance.status,
        'amount': str(instance.amount),
        'gateway': instance.gateway,
        'timestamp': instance.updated_at.isoformat(),
    }
    publish_event(Channels.PAYMENT, payload)
