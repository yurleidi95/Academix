from django.contrib import admin
from .models import SystemAlert

@admin.register(SystemAlert)
class SystemAlertAdmin(admin.ModelAdmin):
    list_display = ('title', 'level', 'target_role', 'recipient_user', 'is_active', 'is_dismissible', 'created_at')
    list_filter = ('level', 'is_active', 'is_dismissible', 'target_role')
    search_fields = ('title', 'message', 'recipient_user__username')
    ordering = ('-created_at',)
