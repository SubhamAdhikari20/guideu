from django.contrib import admin

from .models import Badge, BadgeAward


@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "points", "trigger_event", "is_active")
    list_filter = ("category", "is_active")
    search_fields = ("name", "trigger_event")


@admin.register(BadgeAward)
class BadgeAwardAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "badge", "points_awarded", "created_at")
    list_filter = ("badge__category",)
    search_fields = ("user__username", "badge__name")
    list_select_related = ("user", "badge")
