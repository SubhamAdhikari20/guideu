from django.contrib import admin

from .models import PriceCheck, ScamReport


@admin.register(ScamReport)
class ScamReportAdmin(admin.ModelAdmin):
    list_display = (
        "id", "reporter", "service_type", "region", "overcharge_ratio",
        "scam_severity", "was_flagged_by_app", "status", "verified_by_moderator", "created_at",
    )
    list_filter = ("scam_severity", "status", "was_flagged_by_app", "verified_by_moderator")
    search_fields = ("reporter__username", "service_type")
    list_select_related = ("region", "reporter")
    readonly_fields = ("created_at", "updated_at")


@admin.register(PriceCheck)
class PriceCheckAdmin(admin.ModelAdmin):
    list_display = ("id", "actor", "service_type", "region", "quoted_price_npr", "overcharge_ratio", "is_likely_scam", "source", "created_at")
    list_filter = ("is_likely_scam", "source", "service_type")
    search_fields = ("actor__username", "service_type")
