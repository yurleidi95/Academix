from django.contrib import admin
from .models import AcademicYear, GradeLevel, CourseSection

@admin.register(AcademicYear)
class AcademicYearAdmin(admin.ModelAdmin):
    list_display = ('year', 'name', 'status', 'is_current', 'start_date', 'end_date')
    list_filter = ('status', 'is_current')
    search_fields = ('name', 'year')

@admin.register(GradeLevel)
class GradeLevelAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'level_stage', 'order')
    list_filter = ('level_stage',)
    ordering = ('order',)

@admin.register(CourseSection)
class CourseSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'grade_level', 'academic_year', 'homeroom_teacher', 'capacity', 'is_active')
    list_filter = ('academic_year', 'grade_level', 'is_active')
    search_fields = ('name', 'classroom', 'homeroom_teacher__username')
