from django.contrib import admin
from django.utils.html import format_html
from .models import Room

class RoomAdmin(admin.ModelAdmin):
    # Only display Room-specific fields, but inherit Property fields automatically
    list_display = ('get_owner', "room_category", "price", "location", "status", "is_active_account", "view_details")
    search_fields = ("room_category", "location__name", "price")
    list_filter = ("status", "is_active_account", "room_category")
    ordering = ("-listing_date",)

    def get_queryset(self, request):
        """
        Override to exclude soft-deleted rooms from appearing in the admin panel.
        """
        queryset = super().get_queryset(request)
        return queryset.filter(is_deleted=False)  # Exclude soft-deleted rooms

    def get_owner(self, obj):
        return obj.agent if obj.agent else "N/A"

    get_owner.short_description = "Owner"

    def view_details(self, obj):
        return format_html(
            '<a href="/admin/room/room/{}/change/" class="button" '
            'style="padding:5px 10px; background:#3498db; color:#fff; border-radius:5px;">View</a>',
            obj.property_id
        )

    view_details.short_description = "Actions"

admin.site.register(Room, RoomAdmin)
