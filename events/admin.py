from django.contrib import admin
from .models import Event, EventScheduleDay, EventImportantDate, EventGallery

class EventScheduleDayInline(admin.TabularInline):
    model = EventScheduleDay
    extra = 1

class EventImportantDateInline(admin.TabularInline):
    model = EventImportantDate
    extra = 1

class EventGalleryInline(admin.TabularInline):
    model = EventGallery
    extra = 1

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'location', 'start_date', 'end_date', 'status', 'is_featured', 'created_at')
    list_filter = ('status', 'category', 'is_featured', 'start_date')
    search_fields = ('title', 'location', 'organizer', 'short_description', 'about')
    prepopulated_fields = {'slug': ('title',)}
    inlines = [EventScheduleDayInline, EventImportantDateInline, EventGalleryInline]
    actions = ['approve_events', 'publish_events', 'reject_events']

    def approve_events(self, request, queryset):
        queryset.update(status='approved')
    approve_events.short_description = "Mark selected events as Approved"

    def publish_events(self, request, queryset):
        queryset.update(status='published')
    publish_events.short_description = "Publish selected events publicly"

    def reject_events(self, request, queryset):
        queryset.update(status='rejected')
    reject_events.short_description = "Reject selected events"
