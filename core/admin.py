from django.contrib import admin
from .models import State, City, Locality, UserLocationPreference, FooterSetting, LegalPage

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'slug')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'state', 'is_popular', 'slug')
    list_filter = ('state', 'is_popular')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Locality)
class LocalityAdmin(admin.ModelAdmin):
    list_display = ('name', 'city', 'pincode', 'slug')
    list_filter = ('city__state', 'city')
    search_fields = ('name', 'pincode')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(UserLocationPreference)
class UserLocationPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'city', 'locality', 'updated_at')

@admin.register(FooterSetting)
class FooterSettingAdmin(admin.ModelAdmin):
    list_display = ('site_name', 'tagline', 'contact_email', 'support_email', 'updated_at')

@admin.register(LegalPage)
class LegalPageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'is_active', 'last_updated', 'updated_at')
    list_filter = ('is_active',)
    search_fields = ('title', 'slug', 'content')
    prepopulated_fields = {'slug': ('title',)}
