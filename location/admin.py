from django.contrib import admin
from .models import District, Region, Ward, Street


class StreetAdmin(admin.ModelAdmin):
    list_display = ('name', 'ward')
    search_fields = ('street_id', 'name')
    ordering = ('name',)
    list_per_page = 20

class WardAdmin(admin.ModelAdmin):
    list_display = ('name', 'district')
    search_fields = ('ward_id', 'name')
    ordering = ('name',)
    list_per_page = 20

class DistrictAdmin(admin.ModelAdmin):
    list_display = ('name', 'region')
    search_fields = ('district_id', 'name', 'region__name')
    list_filter = ('region',)
    ordering = ('name',)
    list_per_page = 20


class RegionAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('region_id', 'name')
    ordering = ('name',)
    list_per_page = 20
    


admin.site.register(District, DistrictAdmin)
admin.site.register(Region, RegionAdmin)
admin.site.register(Ward, WardAdmin)
admin.site.register(Street, StreetAdmin)
