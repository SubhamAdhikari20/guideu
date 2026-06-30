from django.contrib import admin

from .models import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ("created_at", "actor", "method", "path", "status_code", "ip_address")
    list_filter = ("method", "status_code")
    search_fields = ("path", "actor__username", "ip_address")
    readonly_fields = ("actor", "method", "path", "status_code", "ip_address", "user_agent", "metadata", "created_at", "updated_at")
    date_hierarchy = "created_at"

    def has_add_permission(self, request) -> bool:  # audit log is append-only via middleware
        return False

    def has_change_permission(self, request, obj=None) -> bool:
        return False
