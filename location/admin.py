from django.contrib import admin

from location.models import Region, District

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name', 'region']
