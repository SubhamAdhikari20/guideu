from __future__ import annotations

from rest_framework import filters, permissions, viewsets

from .models import TourPackage, BookingSession, ItineraryItem
from .serializers import TourPackageSerializer, BookingSessionSerializer, ItineraryItemSerializer


class TourPackageViewSet(viewsets.ModelViewSet):
    queryset = TourPackage.objects.filter(is_active=True).order_by('-created_at')
    serializer_class = TourPackageSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('title', 'description')
    ordering_fields = ('base_price', 'duration_days')


class BookingSessionViewSet(viewsets.ModelViewSet):
    queryset = BookingSession.objects.all().order_by('-created_at')
    serializer_class = BookingSessionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter, filters.OrderingFilter)
    search_fields = ('booking_reference', 'tourist__username', 'assigned_guide__username')
    ordering_fields = ('start_date', 'end_date', 'status')

    def get_queryset(self):
        """Tourists see their own bookings (or the ones assigned to them as a
        guide); staff see everything."""
        qs = super().get_queryset()
        user = self.request.user
        if user.is_staff:
            return qs
        from django.db.models import Q
        return qs.filter(Q(tourist=user) | Q(assigned_guide=user))

    def perform_create(self, serializer):
        serializer.save(tourist=self.request.user)


class ItineraryItemViewSet(viewsets.ModelViewSet):
    queryset = ItineraryItem.objects.all()
    serializer_class = ItineraryItemSerializer
    permission_classes = (permissions.IsAuthenticated,)
