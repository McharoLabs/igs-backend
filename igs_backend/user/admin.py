from django.contrib import admin
from django.utils.html import format_html

from igs_backend.igs_backend import settings
from .models import Agent

class AgentAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone_number", "email", "is_active", "view_details")
    search_fields = ("first_name", "last_name", "phone_number", "email")
    list_filter = ("is_active", "gender")
    ordering = ("-is_active", "first_name")

    fieldsets = (
        (None, {'fields': ('password',)}),
        ("Personal Information", {"fields": ("first_name", "middle_name", "last_name", "gender", "phone_number", "email")}),
        # ("Authentication", {"fields": ("password",)}),
        # ("Profile", {"fields": ("avatar", "is_active")}),
    )

    def get_queryset(self, request):
        """Ensure only agents are displayed in the admin panel"""
        return Agent.objects.all()

    def full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
    
    full_name.short_description = "Full Name"

    def view_details(self, obj):
        """Add a clickable button to view agent details."""
        return format_html('<a href="/admin/user/agent/{}/change/" class="button" style="padding:5px 10px; background:#3498db; color:#fff; border-radius:5px;">View</a>', obj.user_id)
    
    view_details.short_description = "Actions"
    
    def save_model(self, request, obj, form, change):
        if 'password' in form.changed_data:
            obj.set_password(form.cleaned_data["password"])
        super().save_model(request, obj, form, change)

admin.site.register(Agent, AgentAdmin)
