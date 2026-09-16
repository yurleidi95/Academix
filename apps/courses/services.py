from django.db import transaction
from .models import AcademicYear, CourseSection, GradeLevel
from apps.audit.services import log_audit

def get_current_academic_year():
    """Retorna el año lectivo vigente actual o None si no hay ninguno marcado."""
    return AcademicYear.objects.filter(is_current=True).first() or AcademicYear.objects.filter(status=AcademicYear.Status.ACTIVE).first()

@transaction.atomic
def set_current_academic_year(year_id, user=None):
    """
    Establece de manera atómica el año lectivo activo en el sistema,
    desactivando los restantes y auditando el cambio.
    """
    target_year = AcademicYear.objects.select_for_update().get(id=year_id)
    
    # Desmarcar los demás
    AcademicYear.objects.exclude(id=target_year.id).filter(is_current=True).update(is_current=False)
    
    target_year.is_current = True
    target_year.status = AcademicYear.Status.ACTIVE
    target_year.save(update_fields=['is_current', 'status'])

    log_audit(
        action='UPDATE',
        table_name='AcademicYear',
        record_id=target_year.id,
        new_values={'year': target_year.year, 'is_current': True, 'status': target_year.status},
        reason=f'Establecido año {target_year.year} como año lectivo vigente',
        user=user
    )

    return target_year

@transaction.atomic
def create_course_section(academic_year, grade_level, name, classroom='', homeroom_teacher=None, capacity=35, user=None):
    """
    Crea un nuevo grupo o sección escolar garantizando unicidad y trazabilidad.
    """
    section = CourseSection.objects.create(
        academic_year=academic_year,
        grade_level=grade_level,
        name=name,
        classroom=classroom,
        homeroom_teacher=homeroom_teacher,
        capacity=capacity
    )

    log_audit(
        action='INSERT',
        table_name='CourseSection',
        record_id=section.id,
        new_values={
            'name': section.name,
            'year': academic_year.year,
            'grade': grade_level.name,
            'capacity': capacity
        },
        reason=f'Creación de sección académica {name}',
        user=user
    )

    return section
