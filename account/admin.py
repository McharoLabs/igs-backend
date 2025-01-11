# admin.py
from django.contrib import admin
from .models import Account, SubscriptionPlan

class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_id', 'agent', 'plan', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'plan', 'start_date', 'end_date')
    search_fields = ('account_id', 'agent__name', 'plan__name')
    ordering = ('-start_date',)
    date_hierarchy = 'start_date'
    raw_id_fields = ('agent', 'plan')

class SubscriptionPlanAdmin(admin.ModelAdmin):
    list_display = ('subscription_plan_id', 'name', 'price', 'max_houses', 'duration_days')
    list_filter = ('max_houses', 'duration_days')
    search_fields = ('name',)
    ordering = ('name',)
    fieldsets = (
        (None, {
            'fields': ('name', 'price', 'max_houses', 'duration_days')
        }),
    )

admin.site.register(Account, AccountAdmin)
admin.site.register(SubscriptionPlan, SubscriptionPlanAdmin)
