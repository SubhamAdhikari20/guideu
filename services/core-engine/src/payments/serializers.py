from __future__ import annotations

from typing import Any

from rest_framework import serializers

from .models import PaymentTransaction, EscrowLedger


class PaymentTransactionSerializer(serializers.ModelSerializer):
    # The payer is taken from the logged-in user in the view.
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = PaymentTransaction
        fields = ('id', 'user', 'booking', 'amount', 'currency', 'status', 'gateway', 'gateway_reference', 'gateway_metadata', 'created_at')
        read_only_fields = ('status', 'gateway_reference', 'created_at')

    def validate_amount(self, value: Any) -> Any:
        if value <= 0:
            raise serializers.ValidationError('Amount must be positive')
        return value


class EscrowLedgerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EscrowLedger
        fields = ('id', 'transaction', 'entry_type', 'amount', 'balance', 'notes', 'created_at')
