# admin.py
from django.contrib import admin

from subscription_plan.models import SubscriptionPlan
from .models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ('account_id', 'agent', 'plan', 'start_date', 'end_date', 'is_active')
    list_filter = ('is_active', 'plan', 'start_date', 'end_date')
    search_fields = ('account_id', 'agent__name', 'plan__name')
    ordering = ('-start_date',)
    date_hierarchy = 'start_date'
    raw_id_fields = ('agent', 'plan')


admin.site.register(Account, AccountAdmin)
