from django.contrib import admin
from .models import EvaluationCriterion, GradeRecord, PeriodFinalGrade

@admin.register(EvaluationCriterion)
class EvaluationCriterionAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'subject', 'course_section', 'academic_period', 'order')
    list_filter = ('academic_period', 'course_section', 'subject')
    ordering = ('course_section', 'subject', 'order')

@admin.register(GradeRecord)
class GradeRecordAdmin(admin.ModelAdmin):
    list_display = ('student', 'criterion', 'score', 'course_section', 'subject', 'academic_period', 'updated_at')
    list_filter = ('academic_period', 'course_section', 'subject')
    search_fields = ('student__user__username', 'student__user__last_name', 'criterion__name')

@admin.register(PeriodFinalGrade)
class PeriodFinalGradeAdmin(admin.ModelAdmin):
    list_display = ('student', 'course_section', 'subject', 'academic_period', 'final_score', 'performance_level', 'is_approved')
    list_filter = ('academic_period', 'performance_level', 'is_approved')
    search_fields = ('student__user__username', 'student__user__last_name')
