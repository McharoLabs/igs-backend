from django.contrib import admin
from .models import LandImage

@admin.register(LandImage)
class LandImageAdmin(admin.ModelAdmin):
    list_display = ('image_id', 'land', 'image')
