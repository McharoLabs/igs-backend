from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import MessageQueue

class MessageQueueAdmin(admin.ModelAdmin):
    list_display = ("to", "description", "name", "group_name", "view_details")
    search_fields = ("to", "name", "group_name", "description")
    list_filter = ("group_name",)
    ordering = ("-id",)

    fieldsets = (
        ("Message Details", {
            "fields": ("message", "to", "description", "name", "group_name", "payment")
        }),
    )

    def view_details(self, obj):
        """Add a clickable button to view message queue details."""
        change_url = reverse(
            "admin:{}_{}_change".format(obj._meta.app_label, obj._meta.model_name),
            args=[obj.pk]
        )
        return format_html(
            '<a href="{}" class="button" style="padding:5px 10px; background:#3498db; color:#fff; border-radius:5px;">View</a>',
            change_url
        )

    view_details.short_description = "Actions"

admin.site.register(MessageQueue, MessageQueueAdmin)
