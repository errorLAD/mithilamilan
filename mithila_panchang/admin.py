from django.contrib import admin
from .models import (
    PanchangSource, ScannedPanchangPage, PanchangYear, PanchangMonth,
    PanchangDay, Festival, MuhuratCategory, MuhuratDate, PanchangAuditLog, MithilaSong
)

@admin.register(PanchangSource)
class PanchangSourceAdmin(admin.ModelAdmin):
    list_display = ('name', 'year_label', 'publisher', 'editor')

@admin.register(ScannedPanchangPage)
class ScannedPanchangPageAdmin(admin.ModelAdmin):
    list_display = ('page_number', 'title', 'image_path')
    search_fields = ('title', 'ocr_text')

@admin.register(PanchangYear)
class PanchangYearAdmin(admin.ModelAdmin):
    list_display = ('title_hi', 'gregorian_year', 'vikram_samvat', 'saka_samvat', 'king_planet', 'is_active')

@admin.register(PanchangMonth)
class PanchangMonthAdmin(admin.ModelAdmin):
    list_display = ('name_hi', 'name_en', 'month_order', 'gregorian_range_hi')
    list_filter = ('year',)

@admin.register(PanchangDay)
class PanchangDayAdmin(admin.ModelAdmin):
    list_display = ('date', 'mithila_month_name', 'paksha', 'mithila_tithi_name', 'nakshatra_name', 'weekday_name')
    list_filter = ('paksha', 'mithila_month_name')
    search_fields = ('mithila_tithi_name', 'nakshatra_name', 'special_observances')
    date_hierarchy = 'date'

@admin.register(Festival)
class FestivalAdmin(admin.ModelAdmin):
    list_display = ('title_hi', 'date', 'mithila_month_name', 'category')
    list_filter = ('category', 'mithila_month_name')
    search_fields = ('title_hi', 'title_mai', 'title_en', 'short_description')
    date_hierarchy = 'date'

@admin.register(MuhuratCategory)
class MuhuratCategoryAdmin(admin.ModelAdmin):
    list_display = ('name_hi', 'name_en', 'slug', 'icon', 'order')
    prepopulated_fields = {'slug': ('name_en',)}

@admin.register(MuhuratDate)
class MuhuratDateAdmin(admin.ModelAdmin):
    list_display = ('gregorian_date', 'category', 'mithila_month_name', 'tithi_name', 'weekday_name', 'verification_status', 'is_published')
    list_filter = ('category', 'verification_status', 'is_published', 'mithila_month_name')
    search_fields = ('tithi_name', 'nakshatra_name', 'notes', 'source_reference_text')
    date_hierarchy = 'gregorian_date'

@admin.register(PanchangAuditLog)
class PanchangAuditLogAdmin(admin.ModelAdmin):
    list_display = ('timestamp', 'action', 'record_type', 'record_id', 'changed_by')
    list_filter = ('action', 'record_type')

@admin.register(MithilaSong)
class MithilaSongAdmin(admin.ModelAdmin):
    list_display = ('title', 'video_id', 'singer', 'category', 'order', 'is_featured', 'is_published')
    list_filter = ('category', 'is_featured', 'is_published')
    search_fields = ('title', 'video_id', 'singer')
    list_editable = ('order', 'is_featured', 'is_published')

