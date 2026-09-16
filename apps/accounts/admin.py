from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'document_number', 'get_full_name', 'role', 'email', 'is_active', 'is_staff')
    list_filter = ('role', 'is_active', 'is_staff', 'document_type')
    search_fields = ('username', 'document_number', 'first_name', 'last_name', 'email')
    ordering = ('last_name', 'first_name')

    fieldsets = UserAdmin.fieldsets + (
        ('Datos Institucionales y Rol', {
            'fields': ('role', 'document_type', 'document_number', 'phone', 'address', 'avatar', 'must_change_password')
        }),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Datos Institucionales y Rol', {
            'fields': ('role', 'document_type', 'document_number', 'phone', 'address', 'avatar', 'must_change_password')
        }),
    )
