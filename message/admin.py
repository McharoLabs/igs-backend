from django.contrib import admin
from django.utils.html import format_html
from .models import MessageQueue

class MessageQueueAdmin(admin.ModelAdmin):
    list_display = ("to", "description", "name", "group_name", "view_payment_action")
    search_fields = ("to", "name", "group_name", "description")
    list_filter = ("group_name",)
    ordering = ("-id",)

    fieldsets = (
        ("Message Details", {
            "fields": ("message", "to", "description", "name", "group_name", "payment")
        }),
    )

    def view_payment_action(self, obj):
        """Add a clickable button to view payment details."""
        if obj.payment:
            return format_html(
                '<a href="/admin/app_name/payment/{}/change/" class="button" '
                'style="padding:5px 10px; background:#3498db; color:#fff; border-radius:5px;">View Payment</a>',
                obj.payment.payment_id 
            )
        return format_html('<span style="color: red;">No Payment</span>')

    view_payment_action.short_description = "Actions"

admin.site.register(MessageQueue, MessageQueueAdmin)
