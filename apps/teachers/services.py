from django.db import transaction
from .models import TeacherProfile, TeachingAssignment
from apps.courses.models import CourseSection, AcademicYear
from apps.subjects.models import Subject
from apps.audit.services import log_audit

def get_or_create_teacher_profile(user, specialty='Docente de Educación Básica/Media'):
    """Recupera o crea el perfil docente institucional para un usuario con rol TEACHER."""
    profile, _ = TeacherProfile.objects.get_or_create(
        user=user,
        defaults={'specialty': specialty}
    )
    return profile

@transaction.atomic
def assign_teacher_to_subject(teacher, course_section, subject, academic_year, user=None):
    """
    Asigna un docente a una asignatura y grupo escolar con validación de exclusividad y auditoría.
    """
    assignment, created = TeachingAssignment.objects.update_or_create(
        course_section=course_section,
        subject=subject,
        academic_year=academic_year,
        defaults={
            'teacher': teacher,
            'is_active': True,
        }
    )

    action = 'INSERT' if created else 'UPDATE'
    log_audit(
        action=action,
        table_name='TeachingAssignment',
        record_id=assignment.id,
        new_values={
            'teacher': teacher.user.get_full_name() or teacher.user.username,
            'section': course_section.name,
            'subject': subject.name,
            'year': academic_year.year,
        },
        reason=f'Asignación académica de {subject.name} en {course_section.name} a {teacher.user.username}',
        user=user
    )

    return assignment
