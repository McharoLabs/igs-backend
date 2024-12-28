from django.contrib import admin

from booking.models import Booking


@admin.register(Booking)
class HouseBookingAdmin(admin.ModelAdmin):
    list_display = [
        'house', 
        'room', 
        'booking_fee', 
        'is_completed', 
        'listing_date'
    ]
    list_filter = ['is_completed', 'house']
    search_fields = ['booking_id']
    ordering = ['-listing_date']

    def get_house_details(self, obj):
        return f"{obj.house.title} - {obj.room.name if obj.room else 'N/A'}"

    get_house_details.short_description = "House and Room Details"