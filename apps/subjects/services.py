from decimal import Decimal
from django.db import transaction
from .models import KnowledgeArea, Subject, GradeSubject
from apps.audit.services import log_audit

def get_curriculum_for_grade(grade_level):
    """Retorna las asignaturas con su intensidad horaria para un grado."""
    return GradeSubject.objects.filter(grade_level=grade_level).select_related('subject', 'subject__area')

@transaction.atomic
def configure_grade_subject(grade_level, subject, weekly_hours=4, weight_percentage=Decimal('100.00'), user=None):
    """
    Configura o actualiza la intensidad horaria de una asignatura en un grado escolar.
    """
    obj, created = GradeSubject.objects.update_or_create(
        grade_level=grade_level,
        subject=subject,
        defaults={
            'weekly_hours': weekly_hours,
            'weight_percentage': weight_percentage,
        }
    )

    action = 'INSERT' if created else 'UPDATE'
    log_audit(
        action=action,
        table_name='GradeSubject',
        record_id=obj.id,
        new_values={
            'grade': grade_level.name,
            'subject': subject.name,
            'weekly_hours': weekly_hours,
            'weight_percentage': str(weight_percentage),
        },
        reason=f'Configuración curricular: {subject.name} en grado {grade_level.name} ({weekly_hours}h/sem)',
        user=user
    )

    return obj
