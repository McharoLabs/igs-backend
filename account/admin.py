from django.contrib import admin
from account.models import SubscriptionPlan


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = [ 'name', 'price', 'max_houses', 'duration_days']
    list_filter = ['max_houses', 'duration_days']
    search_fields = ['name']
    ordering = ['name']

    fieldsets = (
        (None, {
            'fields': ('name', 'price', 'max_houses', 'duration_days')
        }),
        ('Advanced Options', {
            'classes': ('collapse',),
            'fields': (),
        }),
    )
