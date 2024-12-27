from django.contrib import admin
from .models import District, Region

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('district_id', 'name', 'region')
    search_fields = ('district_id', 'name', 'region__name')
    list_filter = ('region',)
    ordering = ('name',)
    list_per_page = 20

class RegionAdmin(admin.ModelAdmin):
    list_display = ('region_id', 'name')
    search_fields = ('region_id', 'name')
    ordering = ('name',)
    list_per_page = 20

admin.site.register(District, DistrictAdmin)
admin.site.register(Region, RegionAdmin)
