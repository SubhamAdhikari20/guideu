from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import TourPackageViewSet, BookingSessionViewSet, ItineraryItemViewSet

router = DefaultRouter()
router.register(r'packages', TourPackageViewSet, basename='package')
router.register(r'bookings', BookingSessionViewSet, basename='booking')
router.register(r'itinerary-items', ItineraryItemViewSet, basename='itineraryitem')

urlpatterns = [path('', include(router.urls))]
