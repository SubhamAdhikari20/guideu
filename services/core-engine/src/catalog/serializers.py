from __future__ import annotations

from rest_framework import serializers

from .models import (
    CulturalEvent,
    GuideRegistry,
    PricingBenchmark,
    Region,
    TrekkingRoute,
)


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = ("id", "name", "slug", "description", "is_remote", "is_active")
        read_only_fields = ("slug",)


class TrekkingRouteSerializer(serializers.ModelSerializer):
    region = serializers.SlugRelatedField(slug_field="name", queryset=Region.objects.all())
    permit_list = serializers.ReadOnlyField()
    best_season_list = serializers.ReadOnlyField()

    class Meta:
        model = TrekkingRoute
        fields = (
            "id", "external_id", "route_name", "region", "permits_required", "permit_list",
            "difficulty", "difficulty_level", "max_altitude_m", "duration_days",
            "best_seasons", "best_season_list", "seasonal_closure_months",
            "badge_points", "estimated_cost_usd", "is_published", "created_at",
        )
        read_only_fields = ("external_id", "created_at")


class GuideRegistrySerializer(serializers.ModelSerializer):
    language_list = serializers.ReadOnlyField()
    region_list = serializers.ReadOnlyField()
    is_verified = serializers.ReadOnlyField()

    class Meta:
        model = GuideRegistry
        fields = (
            "id", "external_id", "guide_code", "ntb_license_no", "certification",
            "languages_spoken", "language_list", "regions_covered", "region_list",
            "years_experience", "average_rating", "total_trips_completed",
            "verification_status", "is_verified", "is_active", "created_at",
        )
        read_only_fields = ("external_id", "created_at")


class CulturalEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CulturalEvent
        fields = (
            "id", "external_id", "festival_name", "event_type", "start_month",
            "duration_days", "region", "year", "badge_eligible", "significance",
            "badge_points",
        )
        read_only_fields = ("external_id",)


class PricingBenchmarkSerializer(serializers.ModelSerializer):
    region = serializers.SlugRelatedField(slug_field="name", queryset=Region.objects.all())

    class Meta:
        model = PricingBenchmark
        fields = (
            "id", "external_id", "service_type", "region", "season",
            "fair_price_npr", "min_fair_npr", "max_fair_npr", "currency",
            "unit", "source_type", "last_updated",
        )
        read_only_fields = ("external_id",)


class FairPriceQuerySerializer(serializers.Serializer):
    """Validates the `pricing-benchmarks/lookup` query params."""

    service_type = serializers.CharField()
    region = serializers.CharField(required=False, allow_blank=True)
    season = serializers.CharField(required=False, allow_blank=True)


class FairPriceResultSerializer(serializers.Serializer):
    service_type = serializers.CharField()
    region = serializers.CharField(allow_null=True)
    season = serializers.CharField(allow_null=True)
    fair_price_npr = serializers.IntegerField()
    min_fair_npr = serializers.IntegerField()
    max_fair_npr = serializers.IntegerField()
    currency = serializers.CharField()
    sample_size = serializers.IntegerField()
