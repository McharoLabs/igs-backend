from django.contrib import admin
from .models import House
from django.utils.timezone import now
from django.utils.html import format_html

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ['get_owner', 'price', 'category', 'location', 'status', 'listing_date', 'updated_at']
    list_filter = ['category', 'status', 'listing_date', 'agent']
    search_fields = ['title', 'agent__first_name']
    ordering = ['-listing_date']

    def get_owner(self, obj):
        if obj.agent:
            return obj.agent

    get_owner.short_description = "Owner"