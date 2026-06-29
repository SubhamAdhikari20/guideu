from django.contrib import admin

from .models import Review


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "author", "target_kind", "rating", "status", "is_flagged", "created_at")
    list_filter = ("status", "is_flagged", "rating")
    search_fields = ("author__username", "title", "comment")
    list_editable = ("status",)
    readonly_fields = ("created_at", "updated_at")
    actions = ("approve_selected", "reject_selected")

    @admin.action(description="Approve selected reviews")
    def approve_selected(self, request, queryset):
        queryset.update(status=Review.Status.APPROVED)

    @admin.action(description="Reject selected reviews")
    def reject_selected(self, request, queryset):
        queryset.update(status=Review.Status.REJECTED)
