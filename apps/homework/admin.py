from django.contrib import admin
from .models import Homework, HomeworkSubmission

@admin.register(Homework)
class HomeworkAdmin(admin.ModelAdmin):
    list_display = ('title', 'course_section', 'subject', 'due_date', 'teacher', 'is_active')
    list_filter = ('course_section', 'subject', 'academic_period', 'is_active')
    search_fields = ('title', 'description', 'teacher__user__username')

@admin.register(HomeworkSubmission)
class HomeworkSubmissionAdmin(admin.ModelAdmin):
    list_display = ('homework', 'student', 'submitted_at', 'status', 'score')
    list_filter = ('status', 'homework__academic_period', 'homework__course_section')
    search_fields = ('student__user__username', 'homework__title')
