from django.contrib import admin

from booking.models import Booking


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = [
        'property', 
        'customer_name',
        'customer_email',
        'customer_phone_number',
        'has_owner_read', 
        'listing_date'
    ]
    list_filter = ['has_owner_read', 'property']
    search_fields = ['booking_id', 'customer_name', 'customer_phone_number']
    ordering = ['-listing_date']