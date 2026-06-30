from django.contrib import admin

from .models import (
    CulturalEvent,
    GuideRegistry,
    PricingBenchmark,
    Region,
    TrekkingRoute,
)


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_remote", "is_active")
    list_filter = ("is_remote", "is_active")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(TrekkingRoute)
class TrekkingRouteAdmin(admin.ModelAdmin):
    list_display = ("external_id", "route_name", "region", "difficulty", "max_altitude_m", "duration_days", "is_published")
    list_filter = ("difficulty", "region", "is_published")
    search_fields = ("external_id", "route_name", "permits_required")
    list_select_related = ("region",)
    readonly_fields = ("created_at", "updated_at")


@admin.register(GuideRegistry)
class GuideRegistryAdmin(admin.ModelAdmin):
    list_display = ("external_id", "guide_code", "certification", "average_rating", "verification_status", "is_active")
    list_filter = ("certification", "verification_status", "is_active")
    search_fields = ("external_id", "guide_code", "ntb_license_no")
    readonly_fields = ("created_at", "updated_at")


@admin.register(CulturalEvent)
class CulturalEventAdmin(admin.ModelAdmin):
    list_display = ("external_id", "festival_name", "event_type", "region", "year", "start_month", "significance")
    list_filter = ("event_type", "significance", "badge_eligible", "year")
    search_fields = ("external_id", "festival_name", "region")


@admin.register(PricingBenchmark)
class PricingBenchmarkAdmin(admin.ModelAdmin):
    list_display = ("external_id", "service_type", "region", "season", "fair_price_npr", "source_type", "last_updated")
    list_filter = ("service_type", "season", "source_type")
    search_fields = ("external_id", "service_type")
    list_select_related = ("region",)
