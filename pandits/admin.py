from django.contrib import admin
from .models import PanditProfile, PanditGallery, ConsultationRequest

class PanditGalleryInline(admin.TabularInline):
    model = PanditGallery
    extra = 1

@admin.register(PanditProfile)
class PanditProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'profile_type', 'location', 'experience_years', 'whatsapp_number', 'is_verified', 'status', 'created_at')
    list_filter = ('status', 'profile_type', 'is_verified', 'is_featured', 'location')
    search_fields = ('full_name', 'specialization', 'services_offered', 'location', 'languages')
    prepopulated_fields = {'slug': ('full_name',)}
    inlines = [PanditGalleryInline]
    actions = ['approve_profiles', 'verify_profiles', 'reject_profiles', 'suspend_profiles']

    def approve_profiles(self, request, queryset):
        queryset.update(status='approved')
    approve_profiles.short_description = "Approve selected profiles"

    def verify_profiles(self, request, queryset):
        queryset.update(is_verified=True, status='published')
    verify_profiles.short_description = "Verify & Publish selected profiles"

    def reject_profiles(self, request, queryset):
        queryset.update(status='rejected')
    reject_profiles.short_description = "Reject selected profiles"

    def suspend_profiles(self, request, queryset):
        queryset.update(status='suspended')
    suspend_profiles.short_description = "Suspend selected profiles"

@admin.register(ConsultationRequest)
class ConsultationRequestAdmin(admin.ModelAdmin):
    list_display = ('profile', 'user_name', 'user_phone', 'service_required', 'preferred_date', 'status', 'created_at')
    list_filter = ('status', 'location_type', 'created_at')
    search_fields = ('user_name', 'user_phone', 'service_required', 'profile__full_name')
