from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import DateInput
from .models import SiteSettings
from django.db import models

@admin.register(SiteSettings)
class SettingsAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = ('support_phone', 'support_email', 'headquarters', 'booking_fee', 'created_at')
    
    # Fields to filter on
    list_filter = ('created_at', 'booking_fee')  # You can filter by date and other fields
    
    # Search functionality
    search_fields = ('support_phone', 'support_email', 'headquarters')
    
    # Make fields editable directly in the list view (inline editing)
    list_editable = ('booking_fee',)
    
    # Display additional information on hover
    list_display_links = ('support_email',)
    
    # # You can also add custom actions
    # actions = ['reset_booking_fee']

    # # Custom action to reset booking fee
    # def reset_booking_fee(self, request, queryset):
    #     updated_count = queryset.update(booking_fee='0')
    #     self.message_user(request, f'{updated_count} setting(s) updated with booking fee reset to 0.')

    # reset_booking_fee.short_description = 'Reset Booking Fee to 0'

    # Fieldsets for organizing fields in the form view
    fieldsets = (
        (None, {
            'fields': ('support_phone', 'support_email')
        }),
        ('Company Info', {
            'fields': ('headquarters', 'booking_fee'),
            'classes': ('collapse',)  # Makes this section collapsible
        }),
        ('Metadata', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )
    
    # Form widgets for more control over the input fields (e.g., date picker)
    formfield_overrides = {
        models.DateTimeField: {'widget': DateInput(attrs={'type': 'date'})}
    }
    
    # Make some fields read-only (like `created_at`)
    readonly_fields = ('created_at',)

    # Override save_model to prevent adding a second row from the Admin
    def save_model(self, request, obj, form, change):
        if not obj.pk and SiteSettings.objects.exists():
            raise ValidationError("Only one settings row is allowed.")
        super().save_model(request, obj, form, change)