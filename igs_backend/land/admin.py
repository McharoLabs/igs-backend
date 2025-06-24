from django.contrib import admin
from django.utils.html import format_html
from .models import Land

class LandAdmin(admin.ModelAdmin):
    list_display = (
        'land_id', 'agent', 'category', 'land_size', 'price', 'status',
        'is_active_account', 'listing_date', 'view_details'
    )
    list_filter = ('category', 'status', 'is_active_account', 'zoning_type', 'access_road_type')
    search_fields = ('land_id', 'agent__user__first_name', 'agent__user__last_name', 'location__region', 'location__district', 'description')
    ordering = ('-listing_date',)
    list_editable = ('is_active_account',)
    readonly_fields = ('listing_date',)
    list_per_page = 25
    fieldsets = (
        ('Basic Information', {
            'fields': ('agent', 'category', 'land_size', 'price', 'status')
        }),
        ('Location Details', {
            'fields': ('location', 'access_road_type', 'zoning_type')
        }),
        ('Features', {
            'fields': ('utilities', 'description', 'is_active_account', 'is_deleted')
        }),
        ('Metadata', {
            'fields': ('listing_date',)
        }),
    )

    def view_details(self, obj):
        return format_html(
            '<a href="/admin/land/land/{}/change/" class="button" '
            'style="padding:5px 10px; background:#2ecc71; color:#fff; border-radius:5px;">View</a>',
            obj.land_id
        )
    view_details.short_description = "Actions"

admin.site.register(Land, LandAdmin)
