from django.contrib import admin

from .models import Favorite, RecentlyViewed


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "route", "guide", "created_at")
    search_fields = ("user__username",)
    list_select_related = ("route", "guide")


@admin.register(RecentlyViewed)
class RecentlyViewedAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "item_type", "item_id", "created_at")
    list_filter = ("item_type",)
    search_fields = ("user__username", "item_id")
