from django.contrib import admin

from .models import TrekkingPermit


@admin.register(TrekkingPermit)
class TrekkingPermitAdmin(admin.ModelAdmin):
    list_display = ('id', 'applicant', 'permit_type', 'status', 'applied_date', 'created_at')
    list_filter = ('permit_type', 'status')
    search_fields = ('applicant__username',)
    readonly_fields = ('created_at', 'updated_at')
