from django.db import transaction
from .models import StudentProfile, Enrollment
from apps.courses.models import CourseSection, AcademicYear
from apps.audit.services import log_audit

def get_or_create_student_profile(user, student_code=None, parent=None, blood_type='O+'):
    """Recupera o crea el expediente para un usuario con rol STUDENT."""
    if not student_code:
        student_code = f"EST-{user.id:05d}"

    profile, _ = StudentProfile.objects.get_or_create(
        user=user,
        defaults={
            'student_code': student_code,
            'parent': parent,
            'blood_type': blood_type,
        }
    )
    return profile

@transaction.atomic
def enroll_student_in_section(student_profile, course_section, academic_year, user=None):
    """
    Matricula formalmente a un estudiante en un grupo para un año lectivo determinado.
    Garantiza integridad referencial y audita la acción.
    """
    enrollment, created = Enrollment.objects.update_or_create(
        student=student_profile,
        academic_year=academic_year,
        defaults={
            'course_section': course_section,
            'status': Enrollment.Status.ACTIVE,
        }
    )

    action = 'INSERT' if created else 'UPDATE'
    log_audit(
        action=action,
        table_name='Enrollment',
        record_id=enrollment.id,
        new_values={
            'student': student_profile.user.get_full_name() or student_profile.user.username,
            'code': student_profile.student_code,
            'section': course_section.name,
            'year': academic_year.year,
            'status': enrollment.status,
        },
        reason=f'Matrícula de estudiante {student_profile.user.username} en curso {course_section.name} ({academic_year.year})',
        user=user
    )

    return enrollment
