from __future__ import annotations

from rest_framework import permissions, viewsets

from .models import PaymentTransaction, EscrowLedger
from .serializers import PaymentTransactionSerializer, EscrowLedgerSerializer


class PaymentTransactionViewSet(viewsets.ModelViewSet):
    queryset = PaymentTransaction.objects.all().order_by('-created_at')
    serializer_class = PaymentTransactionSerializer
    permission_classes = (permissions.IsAuthenticated,)


class EscrowLedgerViewSet(viewsets.ModelViewSet):
    queryset = EscrowLedger.objects.all().order_by('-created_at')
    serializer_class = EscrowLedgerSerializer
    permission_classes = (permissions.IsAuthenticated,)
