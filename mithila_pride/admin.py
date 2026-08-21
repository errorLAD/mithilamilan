from django.contrib import admin
from .models import MithilaPride, MithilaPrideTimeline, MithilaPrideGallery

class MithilaPrideTimelineInline(admin.TabularInline):
    model = MithilaPrideTimeline
    extra = 1

class MithilaPrideGalleryInline(admin.TabularInline):
    model = MithilaPrideGallery
    extra = 1

@admin.register(MithilaPride)
class MithilaPrideAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'category', 'era_generation', 'place_location', 'status', 'is_featured', 'created_at')
    list_filter = ('status', 'category', 'era_generation', 'is_featured')
    search_fields = ('full_name', 'biography', 'place_location', 'contributions_to_mithila', 'publications_work')
    prepopulated_fields = {'slug': ('full_name',)}
    inlines = [MithilaPrideTimelineInline, MithilaPrideGalleryInline]
    actions = ['approve_personalities', 'publish_personalities', 'reject_personalities']

    def approve_personalities(self, request, queryset):
        queryset.update(status='approved')
    approve_personalities.short_description = "Approve selected personalities"

    def publish_personalities(self, request, queryset):
        queryset.update(status='published')
    publish_personalities.short_description = "Publish selected personalities"

    def reject_personalities(self, request, queryset):
        queryset.update(status='rejected')
    reject_personalities.short_description = "Reject selected personalities"
