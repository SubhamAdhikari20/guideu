from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import PaymentTransactionViewSet, EscrowLedgerViewSet

router = DefaultRouter()
router.register(r'payments', PaymentTransactionViewSet, basename='payment')
router.register(r'escrow', EscrowLedgerViewSet, basename='escrow')

urlpatterns = [path('', include(router.urls))]
