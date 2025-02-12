from django.contrib import admin
from .models import MessageQueue

@admin.register(MessageQueue)
class MessageQueueAdmin(admin.ModelAdmin):
    list_display = ('message_id', 'to', 'description', 'name', 'group_name')
    search_fields = ('message_id', 'to', 'name', 'group_name')
    list_filter = ('group_name', 'payment')
    ordering = ('-id',)
