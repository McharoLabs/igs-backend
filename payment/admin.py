from django.contrib import admin
from django.utils.html import format_html
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'booking_link', 'amount', 'payment_date')
    search_fields = ('payment_id', 'booking__booking_id')
    list_filter = ('booking',)
    ordering = ('-payment_date',)
    list_per_page = 20

    def booking_link(self, obj):
        return format_html('<a href="/admin/house/booking/{}/change/">{}</a>', obj.booking.booking_id, obj.booking.booking_id)
    
    booking_link.short_description = 'Booking ID'

admin.site.register(Payment, PaymentAdmin)
