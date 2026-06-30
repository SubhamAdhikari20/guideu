from django.contrib import admin

from .models import TourPackage, BookingSession, ItineraryItem


@admin.register(TourPackage)
class TourPackageAdmin(admin.ModelAdmin):
    list_display = ('title', 'base_price', 'duration_days', 'capacity', 'is_active', 'created_at')
    list_filter = ('is_active', 'duration_days')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at', 'updated_at')


@admin.register(BookingSession)
class BookingSessionAdmin(admin.ModelAdmin):
    list_display = ('booking_reference', 'tourist', 'tour_package', 'status', 'assigned_guide', 'start_date', 'end_date', 'created_at')
    list_filter = ('status', 'tour_package')
    search_fields = ('booking_reference', 'tourist__username', 'assigned_guide__username')
    readonly_fields = ('created_at', 'updated_at')


class ItineraryInline(admin.TabularInline):
    model = ItineraryItem
    extra = 0
    readonly_fields = ('created_at', 'updated_at')


BookingSessionAdmin.inlines = (ItineraryInline,)
