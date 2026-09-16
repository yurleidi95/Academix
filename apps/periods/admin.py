from django.contrib import admin
from .models import AcademicPeriod

@admin.register(AcademicPeriod)
class AcademicPeriodAdmin(admin.ModelAdmin):
    list_display = ('name', 'number', 'academic_year', 'percentage', 'status', 'start_date', 'end_date')
    list_filter = ('academic_year', 'status')
    ordering = ('academic_year', 'number')
