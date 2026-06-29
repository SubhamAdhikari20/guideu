from __future__ import annotations

import django_filters as filters

from .models import CulturalEvent, GuideRegistry, PricingBenchmark, TrekkingRoute


class TrekkingRouteFilter(filters.FilterSet):
    region = filters.CharFilter(field_name="region__name", lookup_expr="iexact")
    min_duration = filters.NumberFilter(field_name="duration_days", lookup_expr="gte")
    max_duration = filters.NumberFilter(field_name="duration_days", lookup_expr="lte")
    max_altitude = filters.NumberFilter(field_name="max_altitude_m", lookup_expr="lte")
    difficulty_level = filters.NumberFilter(field_name="difficulty_level")

    class Meta:
        model = TrekkingRoute
        fields = ["region", "difficulty", "difficulty_level"]


class GuideRegistryFilter(filters.FilterSet):
    region = filters.CharFilter(field_name="regions_covered", lookup_expr="icontains")
    language = filters.CharFilter(field_name="languages_spoken", lookup_expr="icontains")
    min_rating = filters.NumberFilter(field_name="average_rating", lookup_expr="gte")
    min_experience = filters.NumberFilter(field_name="years_experience", lookup_expr="gte")

    class Meta:
        model = GuideRegistry
        fields = ["certification", "verification_status", "is_active"]


class CulturalEventFilter(filters.FilterSet):
    region = filters.CharFilter(field_name="region", lookup_expr="icontains")
    month = filters.NumberFilter(field_name="start_month")

    class Meta:
        model = CulturalEvent
        fields = ["event_type", "year", "badge_eligible", "significance"]


class PricingBenchmarkFilter(filters.FilterSet):
    region = filters.CharFilter(field_name="region__name", lookup_expr="iexact")

    class Meta:
        model = PricingBenchmark
        fields = ["service_type", "season", "source_type"]
