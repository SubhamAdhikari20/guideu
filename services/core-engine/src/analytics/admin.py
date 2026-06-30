from django.contrib import admin

from .models import UserEvent


@admin.register(UserEvent)
class UserEventAdmin(admin.ModelAdmin):
    list_display = ("id", "actor", "event_type", "item_type", "item_id", "source", "device", "created_at")
    list_filter = ("event_type", "item_type", "device")
    search_fields = ("actor__username", "item_id", "session_id")
    date_hierarchy = "created_at"
