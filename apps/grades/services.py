from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction
from django.core.exceptions import PermissionDenied, ValidationError
from .models import EvaluationCriterion, GradeRecord, PeriodFinalGrade
from apps.audit.services import log_audit

def get_or_create_default_criteria(course_section, subject, academic_period):
    """
    Recupera o inicializa los criterios estándar de evaluación para la asignatura y periodo:
    1. Evaluaciones Escritas y Quices (40.00%)
    2. Talleres, Tareas y Trabajos (40.00%)
    3. Autoevaluación y Actitudinal (20.00%)
    Total = 100.00%
    """
    criteria = list(EvaluationCriterion.objects.filter(
        course_section=course_section,
        subject=subject,
        academic_period=academic_period
    ).order_by('order'))

    if not criteria:
        default_defs = [
            ('Evaluaciones y Quices', Decimal('40.00'), 1),
            ('Talleres y Actividades', Decimal('40.00'), 2),
            ('Actitudinal y Autoevaluación', Decimal('20.00'), 3),
        ]
        criteria = []
        for name, pct, order in default_defs:
            crit = EvaluationCriterion.objects.create(
                course_section=course_section,
                subject=subject,
                academic_period=academic_period,
                name=name,
                percentage=pct,
                order=order
            )
            criteria.append(crit)

    return criteria

def calculate_period_final_grade(student, course_section, subject, academic_period):
    """
    Calcula la nota definitiva del periodo sumando las calificaciones ponderadas.
    Consistencia matemática estricta: Únicamente tipos Decimal y redondeo ROUND_HALF_UP.
    """
    criteria = EvaluationCriterion.objects.filter(
        course_section=course_section,
        subject=subject,
        academic_period=academic_period
    )

    if not criteria.exists():
        return None

    weighted_sum = Decimal('0.00')
    total_percentage_applied = Decimal('0.00')

    for crit in criteria:
        record = GradeRecord.objects.filter(
            student=student,
            course_section=course_section,
            subject=subject,
            academic_period=academic_period,
            criterion=crit
        ).first()

        score = record.score if record else Decimal('1.00')
        weighted_sum += (score * (crit.percentage / Decimal('100.00')))
        total_percentage_applied += crit.percentage

    final_score = weighted_sum.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    # Escala de Desempeño según Decreto 1290 (soporta escalas 0 a 5 y 0 a 10)
    if final_score <= Decimal('5.00'):
        # Escala institucional estándar (0.00 a 5.00)
        if final_score < Decimal('3.00'):
            performance = PeriodFinalGrade.PerformanceLevel.BAJO
            is_approved = False
        elif final_score < Decimal('4.00'):
            performance = PeriodFinalGrade.PerformanceLevel.BASICO
            is_approved = True
        elif final_score < Decimal('4.60'):
            performance = PeriodFinalGrade.PerformanceLevel.ALTO
            is_approved = True
        else:
            performance = PeriodFinalGrade.PerformanceLevel.SUPERIOR
            is_approved = True
    else:
        # Escala institucional extendida (0.00 a 10.00)
        if final_score < Decimal('6.00'):
            performance = PeriodFinalGrade.PerformanceLevel.BAJO
            is_approved = False
        elif final_score < Decimal('8.00'):
            performance = PeriodFinalGrade.PerformanceLevel.BASICO
            is_approved = True
        elif final_score < Decimal('9.20'):
            performance = PeriodFinalGrade.PerformanceLevel.ALTO
            is_approved = True
        else:
            performance = PeriodFinalGrade.PerformanceLevel.SUPERIOR
            is_approved = True

    final_grade, _ = PeriodFinalGrade.objects.update_or_create(
        student=student,
        course_section=course_section,
        subject=subject,
        academic_period=academic_period,
        defaults={
            'final_score': final_score,
            'performance_level': performance,
            'is_approved': is_approved,
        }
    )

    return final_grade


@transaction.atomic
def save_or_update_grade(student, course_section, subject, academic_period, criterion, score, feedback=None, user=None):
    """
    Guarda o actualiza una nota con validación de periodo abierto,
    transacción atómica, auditoría inmutable y recálculo automático de la definitiva.
    Soporta escalas de 0.00 a 5.00 y de 0.00 a 10.00.
    """
    if not academic_period.is_editable:
        raise PermissionDenied(f"El periodo {academic_period.name} está cerrado o bloqueado. No se pueden alterar calificaciones.")

    score_str = str(score).strip().replace(',', '.')
    score_dec = Decimal(score_str).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    if score_dec < Decimal('0.00') or score_dec > Decimal('10.00'):
        raise ValidationError("La calificación debe encontrarse en el rango permitido (0.00 a 5.00 o hasta 10.00).")


    record, created = GradeRecord.objects.select_for_update().get_or_create(
        student=student,
        course_section=course_section,
        subject=subject,
        academic_period=academic_period,
        criterion=criterion,
        defaults={'score': score_dec, 'feedback': feedback, 'graded_by': user}
    )

    old_score = None if created else record.score
    if not created:
        record.score = score_dec
        if feedback is not None:
            record.feedback = feedback
        record.graded_by = user
        record.save()

    # Auditoría inmutable de la nota
    action = 'INSERT' if created else 'UPDATE'
    log_audit(
        action=action,
        table_name='GradeRecord',
        record_id=record.id,
        old_values={'score': str(old_score) if old_score else None},
        new_values={'score': str(score_dec), 'criterion': criterion.name},
        reason=f'Calificación registrada para {student.user.username} en {criterion.name} ({subject.code}): {score_dec}',
        user=user
    )

    # Recalcular definitiva del periodo en tiempo real
    final_grade = calculate_period_final_grade(student, course_section, subject, academic_period)

    return record, final_grade
