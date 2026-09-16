from django.contrib import admin
from .models import KnowledgeArea, Subject, GradeSubject

@admin.register(KnowledgeArea)
class KnowledgeAreaAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')
    ordering = ('order',)

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'area')
    list_filter = ('area',)
    search_fields = ('name', 'code')

@admin.register(GradeSubject)
class GradeSubjectAdmin(admin.ModelAdmin):
    list_display = ('subject', 'grade_level', 'weekly_hours', 'weight_percentage')
    list_filter = ('grade_level', 'subject__area')
    ordering = ('grade_level', 'subject')
