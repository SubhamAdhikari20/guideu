from __future__ import annotations

from drf_spectacular.utils import OpenApiParameter, extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from src.common.permissions import IsAdminOrReadOnly

from .filters import (
    CulturalEventFilter,
    GuideRegistryFilter,
    PricingBenchmarkFilter,
    TrekkingRouteFilter,
)
from .models import (
    CulturalEvent,
    GuideRegistry,
    PricingBenchmark,
    Region,
    TrekkingRoute,
)
from .serializers import (
    CulturalEventSerializer,
    FairPriceQuerySerializer,
    FairPriceResultSerializer,
    GuideRegistrySerializer,
    PricingBenchmarkSerializer,
    RegionSerializer,
    TrekkingRouteSerializer,
)


class RegionViewSet(viewsets.ModelViewSet):
    queryset = Region.objects.filter(is_active=True)
    serializer_class = RegionSerializer
    permission_classes = (IsAdminOrReadOnly,)
    search_fields = ("name",)
    ordering_fields = ("name",)


class TrekkingRouteViewSet(viewsets.ModelViewSet):
    serializer_class = TrekkingRouteSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = TrekkingRouteFilter
    search_fields = ("route_name", "region__name", "permits_required")
    ordering_fields = ("difficulty_level", "duration_days", "max_altitude_m", "estimated_cost_usd", "badge_points")

    def get_queryset(self):
        qs = TrekkingRoute.objects.select_related("region")
        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(is_published=True)
        return qs


class GuideRegistryViewSet(viewsets.ModelViewSet):
    serializer_class = GuideRegistrySerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = GuideRegistryFilter
    search_fields = ("guide_code", "ntb_license_no", "languages_spoken", "regions_covered")
    ordering_fields = ("average_rating", "years_experience", "total_trips_completed")

    def get_queryset(self):
        qs = GuideRegistry.objects.all()
        if not (self.request.user and self.request.user.is_staff):
            qs = qs.filter(is_active=True)
        return qs


class CulturalEventViewSet(viewsets.ModelViewSet):
    queryset = CulturalEvent.objects.all()
    serializer_class = CulturalEventSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = CulturalEventFilter
    search_fields = ("festival_name", "region")
    ordering_fields = ("start_month", "year", "badge_points")


class PricingBenchmarkViewSet(viewsets.ModelViewSet):
    queryset = PricingBenchmark.objects.select_related("region")
    serializer_class = PricingBenchmarkSerializer
    permission_classes = (IsAdminOrReadOnly,)
    filterset_class = PricingBenchmarkFilter
    search_fields = ("service_type",)
    ordering_fields = ("fair_price_npr", "last_updated")

    @extend_schema(
        parameters=[
            OpenApiParameter("service_type", str, required=True),
            OpenApiParameter("region", str, required=False),
            OpenApiParameter("season", str, required=False),
        ],
        responses=FairPriceResultSerializer,
        description="Aggregated fair-price range for a service. Powers transparent "
        "pricing and is the deterministic fallback for the anti-scam check.",
    )
    @action(detail=False, methods=["get"], url_path="lookup", permission_classes=[AllowAny])
    def lookup(self, request):
        query = FairPriceQuerySerializer(data=request.query_params)
        query.is_valid(raise_exception=True)
        result = PricingBenchmark.fair_price_for(
            service_type=query.validated_data["service_type"],
            region_name=query.validated_data.get("region") or None,
            season=query.validated_data.get("season") or None,
        )
        if result is None:
            raise NotFound("No benchmark available for the requested service.")
        return Response(FairPriceResultSerializer(result).data)
