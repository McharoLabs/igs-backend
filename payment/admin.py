from django.contrib import admin
from django.utils.html import format_html
from .models import Payment

class PaymentAdmin(admin.ModelAdmin):
    list_display = ('payment_id', 'transaction_link', 'amount', 'payment_date')
    search_fields = ('payment_id', 'transaction__transaction_id')
    list_filter = ('transaction')
    ordering = ('-payment_date',)
    list_per_page = 20

    def transaction_link(self, obj):
        return format_html('<a href="/admin/house/housetransaction/{}/change/">{}</a>', obj.transaction.transaction_id, obj.transaction.transaction_id)
    
    transaction_link.short_description = 'Transaction ID'

admin.site.register(Payment, PaymentAdmin)
