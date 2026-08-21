from django.contrib import admin
from .models import DriverProfile

@admin.register(DriverProfile)
class DriverProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'vehicle_type', 'vehicle_model', 'service_area', 'mobile_number', 'is_verified', 'status', 'created_at')
    list_filter = ('status', 'vehicle_type', 'is_verified', 'is_featured', 'service_area')
    search_fields = ('full_name', 'vehicle_model', 'vehicle_number', 'service_area', 'mobile_number')
    prepopulated_fields = {'slug': ('full_name',)}
    actions = ['approve_drivers', 'verify_drivers', 'reject_drivers', 'suspend_drivers']

    def approve_drivers(self, request, queryset):
        queryset.update(status='approved')
    approve_drivers.short_description = "Approve selected drivers"

    def verify_drivers(self, request, queryset):
        queryset.update(is_verified=True, status='published')
    verify_drivers.short_description = "Verify & Publish selected drivers"

    def reject_drivers(self, request, queryset):
        queryset.update(status='rejected')
    reject_drivers.short_description = "Reject selected drivers"

    def suspend_drivers(self, request, queryset):
        queryset.update(status='suspended')
    suspend_drivers.short_description = "Suspend selected drivers"
