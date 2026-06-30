from __future__ import annotations

from decimal import Decimal
from typing import Any

from django.core.exceptions import ValidationError
from django.db import models

from src.authentication.models import TimeStampedModel


class PaymentTransaction(TimeStampedModel):
    """Records payment attempts and results from external gateways."""

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        SUCCESS = 'SUCCESS', 'Success'
        FAILED = 'FAILED', 'Failed'
        REFUNDED = 'REFUNDED', 'Refunded'

    class Gateway(models.TextChoices):
        ESEWA = 'ESEWA', 'eSewa'
        KHALTI = 'KHALTI', 'Khalti'
        OTHER = 'OTHER', 'Other'

    user = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='payments', db_index=True)
    booking = models.ForeignKey('bookings.BookingSession', on_delete=models.SET_NULL, null=True, blank=True, related_name='payments', db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    currency = models.CharField(max_length=8, default='NPR')
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING, db_index=True)
    gateway = models.CharField(max_length=16, choices=Gateway.choices, default=Gateway.OTHER, db_index=True)
    gateway_reference = models.CharField(max_length=128, blank=True, null=True, db_index=True)
    gateway_metadata = models.JSONField(blank=True, null=True, help_text='Raw gateway response or tokens')

    class Meta:
        verbose_name = 'payment transaction'
        verbose_name_plural = 'payment transactions'

    def clean(self) -> None:
        if self.amount <= 0:
            raise ValidationError({'amount': 'Amount must be positive.'})

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        super().save(*args, **kwargs)


class EscrowLedger(TimeStampedModel):
    """Simple escrow ledger for platform-managed funds for bookings.

    Each entry is an append-only ledger record reflecting credits/debits.
    """

    class EntryType(models.TextChoices):
        CREDIT = 'CREDIT', 'Credit'
        DEBIT = 'DEBIT', 'Debit'

    transaction = models.ForeignKey('payments.PaymentTransaction', on_delete=models.CASCADE, related_name='ledger_entries', db_index=True)
    entry_type = models.CharField(max_length=8, choices=EntryType.choices, db_index=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    balance = models.DecimalField(max_digits=12, decimal_places=2, help_text='Resulting balance after entry')
    notes = models.TextField(blank=True)

    class Meta:
        verbose_name = 'escrow ledger entry'
        verbose_name_plural = 'escrow ledger entries'

    def clean(self) -> None:
        if self.amount <= 0:
            raise ValidationError({'amount': 'Amount must be positive.'})

    def save(self, *args: Any, **kwargs: Any) -> None:
        self.full_clean()
        super().save(*args, **kwargs)
