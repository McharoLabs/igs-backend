from django.contrib import admin
from .models import Agent, LandLord, Tenant

class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'middle_name', 'last_name', 'phone_number', 'gender', 'username', 'email', 'is_verified', 'is_active')
    search_fields = ('first_name', 'last_name', 'email', 'username', 'phone_number')
    list_filter = ('is_verified', 'is_active', 'gender')
    ordering = ('-user_id',)
    list_per_page = 20

class AgentAdmin(UserAdmin):
    list_display = UserAdmin.list_display
    search_fields = UserAdmin.search_fields
    list_filter = UserAdmin.list_filter

class LandLordAdmin(UserAdmin):
    list_display = UserAdmin.list_display
    search_fields = UserAdmin.search_fields
    list_filter = UserAdmin.list_filter

class TenantAdmin(UserAdmin):
    list_display = UserAdmin.list_display
    search_fields = UserAdmin.search_fields
    list_filter = UserAdmin.list_filter

admin.site.register(Agent, AgentAdmin)
admin.site.register(LandLord, LandLordAdmin)
admin.site.register(Tenant, TenantAdmin)
