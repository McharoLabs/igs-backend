from django.contrib import admin
from django.utils.html import format_html
from .models import SubscriptionPlan

class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ("name", "price_display", "max_houses", "duration_days", "is_visible", "is_free", "view_details")
    search_fields = ("name",)
    list_filter = ("is_visible", "is_free")
    ordering = ("-is_visible", "name")

    fieldsets = (
        ("Plan Information", {"fields": ("name", "price", "max_houses", "duration_days", "is_visible", "is_free")}),
    )

    def get_queryset(self, request):
        """Ensure only subscription plans are displayed in the admin panel"""
        return SubscriptionPlan.objects.all()

    def price_display(self, obj):
        """Display the price with a currency symbol."""
        return format_html(
            '<span style="font-weight: bold; color: green;">{} TZS</span>',
            obj.price
        )
    
    price_display.short_description = "Price"

    def view_details(self, obj):
        """Add a clickable button to view subscription plan details."""
        return format_html(
            '<a href="/admin/subscription_plan/subscriptionplan/{}/change/" class="button" style="padding:5px 10px; background:#3498db; color:#fff; border-radius:5px;">View</a>',
            obj.subscription_plan_id
        )

    view_details.short_description = "Actions"

admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
