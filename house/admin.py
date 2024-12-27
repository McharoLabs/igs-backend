from django.contrib import admin
from .models import House, Room, HouseTransaction, TenantRoom
from django.utils.timezone import now
from django.utils.html import format_html

@admin.register(House)
class HouseAdmin(admin.ModelAdmin):
    list_display = ['title', 'get_owner', 'price', 'category', 'location', 'status', 'listing_date', 'updated_at']
    list_filter = ['category', 'status', 'listing_date', 'agent', 'landlord']
    search_fields = ['title', 'agent__first_name', 'landlord__first_name']
    ordering = ['-listing_date']

    def get_owner(self, obj):
        if obj.agent:
            return obj.agent
        elif obj.landlord:
            return obj.landlord
        return "No owner assigned"

    get_owner.short_description = "Owner"


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = [
        'room_number', 
        'house', 
        'room_category', 
        'price', 
        'status', 
        'current_check_in_date', 
        'current_check_out_date', 
        'current_tenant'
    ]
    list_filter = ['room_category', 'status', 'house']
    search_fields = ['room_number', 'house__title']
    ordering = ['house', 'room_number']
    list_per_page = 20

    def current_check_in_date(self, obj):
        today = now().date()
        tenant_room = TenantRoom.objects.filter(
            room=obj, 
            check_in_date__lte=today, 
            check_out_date__gte=today
        ).first()
        return tenant_room.check_in_date if tenant_room else "N/A"

    current_check_in_date.short_description = "Check-In Date"

    def current_check_out_date(self, obj):
        today = now().date()
        tenant_room = TenantRoom.objects.filter(
            room=obj, 
            check_in_date__lte=today, 
            check_out_date__gte=today
        ).first()
        return tenant_room.check_out_date if tenant_room else "N/A"

    current_check_out_date.short_description = "Check-Out Date"

    def current_tenant(self, obj):
        today = now().date()
        tenants = TenantRoom.objects.filter(
            room=obj, 
            check_in_date__lte=today, 
            check_out_date__gte=today
        )
        if tenants.exists():
            return format_html(
                "<br>".join([f"{tenant.tenant}" for tenant in tenants])
            )
        return "No tenants"

    current_tenant.short_description = "Current Tenant(s)"
    
    
@admin.register(HouseTransaction)
class HouseTransactionAdmin(admin.ModelAdmin):
    list_display = [
        'house', 
        'room', 
        'tenant', 
        'booking_fee', 
        'amount', 
        'transaction_type', 
        'is_completed', 
        'listing_date'
    ]
    list_filter = ['transaction_type', 'is_completed', 'house', 'tenant']
    search_fields = ['transaction_id', 'tenant__first_name', 'tenant__last_name']
    ordering = ['-listing_date']

    def get_house_details(self, obj):
        return f"{obj.house.title} - {obj.room.name if obj.room else 'N/A'}"

    get_house_details.short_description = "House and Room Details"