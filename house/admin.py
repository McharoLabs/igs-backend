from django.contrib import admin
from django.utils.html import format_html
from .models import House


class HouseAdmin(admin.ModelAdmin):
    list_display = ('get_owner', 'price', 'category', 'location', 'status', 'is_active_account', 'view_details')
    
    search_fields = ('category', 'location__name', 'price', 'agent__first_name')
    
    list_filter = ('status', 'is_active_account', 'category')
    ordering = ('-listing_date',)

    def get_owner(self, obj):
        if obj.agent:
            return obj.agent

    get_owner.short_description = "Owner"

    def view_details(self, obj):
        return format_html(
            '<a href="/admin/house/house/{}/change/" class="button" style="padding:5px 10px; background:#3498db; color:#fff; border-radius:5px;">View</a>',
            obj.property_id
        )
    
    view_details.short_description = "Actions"

admin.site.register(House, HouseAdmin)
