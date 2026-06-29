from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CulturalEventViewSet,
    GuideRegistryViewSet,
    PricingBenchmarkViewSet,
    RegionViewSet,
    TrekkingRouteViewSet,
)

router = DefaultRouter()
router.register(r"regions", RegionViewSet, basename="region")
router.register(r"routes", TrekkingRouteViewSet, basename="route")
router.register(r"guides-registry", GuideRegistryViewSet, basename="guideregistry")
router.register(r"events", CulturalEventViewSet, basename="culturalevent")
router.register(r"pricing-benchmarks", PricingBenchmarkViewSet, basename="pricingbenchmark")

urlpatterns = [path("", include(router.urls))]
