from django.contrib import admin
from django.utils.html import format_html
from .models import Account

class AccountAdmin(admin.ModelAdmin):
    list_display = ('get_agent_full_name', 'plan_name', 'start_date', 'end_date', 'is_active', 'view_details')
    search_fields = ('agent__first_name', 'agent__last_name', 'plan__name', 'is_active')
    list_filter = ('is_active', 'plan')
    ordering = ('-start_date',)

    def get_agent_full_name(self, obj):
        if obj.agent:
            return obj.agent.full_name
        return "No Agent"
    
    get_agent_full_name.short_description = "Agent"

    def plan_name(self, obj):
        if obj.plan:
            return obj.plan.name
        return "No Plan"
    
    plan_name.short_description = "Subscription Plan"
    
    def view_details(self, obj):
        return format_html(
            '<a href="/admin/account/account/{}/change/" class="button" style="padding:5px 10px; background:#3498db; color:#fff; border-radius:5px;">View</a>', 
            obj.account_id
        )
    
    view_details.short_description = "Actions"

admin.site.register(Account, AccountAdmin)
