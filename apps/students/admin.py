from django.contrib import admin
from .models import StudentProfile, Enrollment

@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('student_code', 'user', 'parent', 'blood_type', 'eps')
    search_fields = ('student_code', 'user__username', 'user__first_name', 'user__last_name', 'parent__username')

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course_section', 'academic_year', 'status', 'enrollment_date')
    list_filter = ('academic_year', 'status', 'course_section__grade_level')
    search_fields = ('student__student_code', 'student__user__username', 'course_section__name')
