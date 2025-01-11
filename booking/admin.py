from django.contrib import admin

from booking.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'property', 
        'booking_fee', 
        'has_owner_read', 
        'listing_date'
    ]
    list_filter = ['has_owner_read', 'property']
    search_fields = ['booking_id']
    ordering = ['-listing_date']