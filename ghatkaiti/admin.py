from django.contrib import admin
from .models import MatrimonialProfile, ProfileReport

@admin.register(MatrimonialProfile)
class MatrimonialProfileAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'looking_for', 'gender', 'age', 'education', 'profession', 'location', 'status', 'created_at')
    list_filter = ('status', 'looking_for', 'gender', 'is_verified', 'is_featured', 'location')
    search_fields = ('full_name', 'education', 'profession', 'location', 'native_place', 'contact_person_name', 'whatsapp_number')
    prepopulated_fields = {'slug': ('full_name',)}
    actions = ['approve_profiles', 'verify_profiles', 'reject_profiles']

    def approve_profiles(self, request, queryset):
        queryset.update(status='approved')
    approve_profiles.short_description = "Approve selected matrimonial posts"

    def verify_profiles(self, request, queryset):
        queryset.update(is_verified=True, status='published')
    verify_profiles.short_description = "Verify & Publish selected matrimonial posts"

    def reject_profiles(self, request, queryset):
        queryset.update(status='rejected')
    reject_profiles.short_description = "Reject selected matrimonial posts"

@admin.register(ProfileReport)
class ProfileReportAdmin(admin.ModelAdmin):
    list_display = ('profile', 'reason', 'reporter_name', 'reporter_email', 'created_at')
    list_filter = ('reason', 'created_at')
    search_fields = ('profile__full_name', 'details', 'reporter_name', 'reporter_email')
