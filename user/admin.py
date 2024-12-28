from django.contrib import admin

class UserAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'middle_name', 'last_name', 'phone_number', 'gender', 'email', 'is_verified', 'is_active')
    search_fields = ('first_name', 'last_name', 'email', 'phone_number')
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
