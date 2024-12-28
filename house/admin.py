from django.contrib import admin
from .models import House, Room
from django.utils.timezone import now
from django.utils.html import format_html

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_owner', 'price', 'category', 'location', 'status', 'listing_date', 'updated_at']
    list_filter = ['category', 'status', 'listing_date', 'agent', 'landlord']
    search_fields = ['title', 'agent__first_name', 'landlord__first_name']
    ordering = ['-listing_date']

    def get_owner(self, obj):
        if obj.agent:
            return obj.agent
        elif obj.landlord:
            return obj.landlord
        return "No owner assigned"

    get_owner.short_description = "Owner"


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = [
        'room_number', 
        'house', 
        'room_category', 
        'price', 
        'status'
    ]
    list_filter = ['room_category', 'status', 'house']
    search_fields = ['room_number', 'house__title']
    ordering = ['house', 'room_number']
    list_per_page = 20