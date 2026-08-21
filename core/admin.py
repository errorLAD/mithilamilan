from django.contrib import admin
from .models import State, City, Locality, UserLocationPreference

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
