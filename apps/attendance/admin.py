from django.contrib import admin
from .models import AttendanceSession, AttendanceRecord

@admin.register(AttendanceSession)
class AttendanceSessionAdmin(admin.ModelAdmin):
    list_display = ('course_section', 'subject', 'date', 'academic_period', 'hours_count', 'recorded_by')
    list_filter = ('academic_period', 'course_section', 'subject', 'date')
    ordering = ('-date',)

@admin.register(AttendanceRecord)
class AttendanceRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'session', 'status', 'is_justified', 'updated_at')
    list_filter = ('status', 'is_justified', 'session__academic_period', 'session__course_section')
    search_fields = ('student__user__username', 'student__student_code', 'justification')
