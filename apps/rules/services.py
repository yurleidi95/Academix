from decimal import Decimal, ROUND_HALF_UP
from django.db import transaction
from django.core.exceptions import PermissionDenied, ValidationError
from django.utils import timezone
from .models import PromotionRule, AnnualFinalGrade, AcademicClosingLog
from apps.periods.models import AcademicPeriod
from apps.courses.models import AcademicYear, CourseSection
from apps.subjects.models import Subject
from apps.students.models import StudentProfile, Enrollment
from apps.grades.models import PeriodFinalGrade
from apps.attendance.models import AttendanceRecord
from apps.attendance.services import calculate_student_absence_stats
from apps.audit.services import log_audit

def get_or_create_promotion_rule(academic_year):
    """
    Obtiene o crea la regla institucional de promoción vigente para el año lectivo.
    """
    rule, _ = PromotionRule.objects.get_or_create(
        academic_year=academic_year,
        defaults={
            'min_passing_grade': Decimal('3.00'),
            'max_failed_subjects': 2,
            'max_absence_percentage': Decimal('20.00'),
            'is_active': True,
        }
    )
    return rule

@transaction.atomic
def close_academic_period(period, user, reason='Cierre formal de periodo lectivo', rector_signature_authorized=True):
    """
    Cierra un periodo lectivo, impidiendo futuras alteraciones de notas y asistencias,
    y registrando la autorización de firma automática de la rectora en boletines.
    """
    if not (user.is_admin_role or user.is_rector):
        raise PermissionDenied("Solo el Rector o Administrador del sistema pueden autorizar el cierre de un periodo.")

    if period.status == AcademicPeriod.Status.CLOSED:
        raise ValidationError(f"El periodo {period.name} ya se encuentra cerrado.")

    period.status = AcademicPeriod.Status.CLOSED
    period.save()

    # Log de cierre formal
    AcademicClosingLog.objects.create(
        academic_year=period.academic_year,
        academic_period=period,
        closing_type=AcademicClosingLog.ClosingType.PERIOD,
        closed_by=user,
        rector_signature_authorized=rector_signature_authorized,
        observations=reason
    )

    log_audit(
        action='UPDATE',
        table_name='AcademicPeriod',
        record_id=period.id,
        old_values={'status': 'ACTIVE'},
        new_values={'status': 'CLOSED'},
        reason=f"Cierre formal del periodo {period.name} ({period.academic_year.year}): {reason}",
        user=user
    )
    return period

@transaction.atomic
def reopen_academic_period(period, user, reason):
    """
    Reabre un periodo cerrado. Requiere autorización directiva y justificación obligatoria.
    """
    if not (user.is_admin_role or user.is_rector):
        raise PermissionDenied("Solo el Rector o Administrador del sistema pueden reabrir un periodo cerrado.")

    if not reason or len(reason.strip()) < 10:
        raise ValidationError("Debe suministrar un motivo justificado detallado para reabrir el periodo.")

    old_status = period.status
    period.status = AcademicPeriod.Status.ACTIVE
    period.save()

    log_audit(
        action='UPDATE',
        table_name='AcademicPeriod',
        record_id=period.id,
        old_values={'status': old_status},
        new_values={'status': 'ACTIVE'},
        reason=f"REAPERTURA EXTRAORDINARIA del periodo {period.name}: {reason}",
        user=user
    )
    return period

def calculate_annual_final_grades_for_student(student, course_section, academic_year):
    """
    Calcula las notas definitivas anuales de un estudiante para todas las asignaturas de su curso.
    Pondera los periodos lectivos según su porcentaje institucional con precisión Decimal.
    """
    rule = get_or_create_promotion_rule(academic_year)
    periods = list(AcademicPeriod.objects.filter(academic_year=academic_year).order_by('number'))

    # Obtener todas las asignaturas cursadas por la sección
    subject_ids = PeriodFinalGrade.objects.filter(
        course_section=course_section,
        academic_period__in=periods
    ).values_list('subject_id', flat=True).distinct()

    annual_grades = []

    for sub_id in subject_ids:
        subject = Subject.objects.get(id=sub_id)
        period_grades = PeriodFinalGrade.objects.filter(
            student=student,
            course_section=course_section,
            subject=subject,
            academic_period__in=periods
        ).select_related('academic_period')

        if not period_grades.exists():
            continue

        weighted_sum = Decimal('0.00')
        total_percentage = Decimal('0.00')

        for pg in period_grades:
            pct = pg.academic_period.percentage
            weighted_sum += (pg.final_score * (pct / Decimal('100.00')))
            total_percentage += pct

        # Si no se han cursado todos los periodos, ponderar sobre el porcentaje acumulado
        if total_percentage > Decimal('0.00'):
            annual_score = ((weighted_sum / total_percentage) * Decimal('100.00')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            annual_score = Decimal('1.00')

        # Nivel de desempeño Decreto 1290
        if annual_score < Decimal('3.00'):
            perf = AnnualFinalGrade.PerformanceLevel.BAJO
            is_app = False
        elif annual_score < Decimal('4.00'):
            perf = AnnualFinalGrade.PerformanceLevel.BASICO
            is_app = True
        elif annual_score < Decimal('4.60'):
            perf = AnnualFinalGrade.PerformanceLevel.ALTO
            is_app = True
        else:
            perf = AnnualFinalGrade.PerformanceLevel.SUPERIOR
            is_app = True

        annual_grade, _ = AnnualFinalGrade.objects.update_or_create(
            student=student,
            course_section=course_section,
            subject=subject,
            academic_year=academic_year,
            defaults={
                'final_score': annual_score,
                'performance_level': perf,
                'is_approved': is_app,
            }
        )
        annual_grades.append(annual_grade)

    return annual_grades

def evaluate_student_promotion(student, course_section, academic_year):
    """
    Evalúa la promoción de grado de un estudiante conforme a las directrices del Decreto 1290:
    1. Si reprueba 3 o más asignaturas -> FAILED (No Promovido).
    2. Si supera el 20% de inasistencias en el año lectivo -> FAILED (Pérdida por Inasistencia).
    3. Si reprueba 1 o 2 materias -> PROMOTED (con asignaturas pendientes para nivelación).
    4. Si aprueba todas -> PROMOTED (Promovido con éxito).
    """
    rule = get_or_create_promotion_rule(academic_year)
    annual_grades = calculate_annual_final_grades_for_student(student, course_section, academic_year)

    failed_grades = [g for g in annual_grades if not g.is_approved]
    failed_count = len(failed_grades)

    # Cálculo acumulado de ausencias de todo el año lectivo
    records = AttendanceRecord.objects.filter(
        student=student,
        session__course_section=course_section,
        session__academic_period__academic_year=academic_year
    ).select_related('session')

    total_sessions = records.count()
    if total_sessions > 0:
        unjustified = records.filter(status=AttendanceRecord.Status.UNJUSTIFIED).count()
        lates = records.filter(status=AttendanceRecord.Status.LATE).count()
        justified = records.filter(status=AttendanceRecord.Status.JUSTIFIED).count()
        equivalent = Decimal(str(unjustified)) + (Decimal(str(lates)) * Decimal('0.33')) + (Decimal(str(justified)) * Decimal('0.50'))
        absence_percentage = ((equivalent / Decimal(str(total_sessions))) * Decimal('100.00')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    else:
        absence_percentage = Decimal('0.00')

    # Dictamen de promoción
    if failed_count > rule.max_failed_subjects:
        status = Enrollment.Status.FAILED
        is_promoted = False
        failed_names = ", ".join([f"{g.subject.name} ({g.final_score})" for g in failed_grades])
        reason = f"No promovido: Reprobó {failed_count} asignaturas ({failed_names}). Supera el límite de {rule.max_failed_subjects} materias permitidas."
    elif absence_percentage >= rule.max_absence_percentage:
        status = Enrollment.Status.FAILED
        is_promoted = False
        reason = f"No promovido por ausentismo: {absence_percentage}% de inasistencias acumuladas en el año lectivo (Límite institucional: {rule.max_absence_percentage}%)."
    else:
        status = Enrollment.Status.PROMOTED
        is_promoted = True
        if failed_count > 0:
            failed_names = ", ".join([f"{g.subject.name} ({g.final_score})" for g in failed_grades])
            reason = f"Promovido con compromisos académicos: Asignaturas pendientes ({failed_names})."
        else:
            reason = "Promovido satisfactoriamente con todas las asignaturas aprobadas."

    return {
        'student': student,
        'is_promoted': is_promoted,
        'status': status,
        'failed_count': failed_count,
        'failed_grades': failed_grades,
        'absence_percentage': absence_percentage,
        'reason': reason,
        'annual_grades': annual_grades,
    }

@transaction.atomic
def execute_annual_closing(academic_year, user, observations='Cierre formal definitivo del año lectivo'):
    """
    Ejecuta el cierre anual definitivo de un año lectivo escolar:
    1. Evalúa y dictamina la promoción de cada estudiante matriculado.
    2. Actualiza los estados de Enrollment a PROMOTED o FAILED.
    3. Bloquea todos los periodos del año (LOCKED).
    4. Cierra el año lectivo (CLOSED) y desactiva su vigencia (is_current=False).
    5. Registra bitácoras inmutables en AcademicClosingLog y AuditLog.
    """
    if not (user.is_admin_role or user.is_rector):
        raise PermissionDenied("Solo el Rector o Administrador del sistema pueden ejecutar el cierre definitivo del año lectivo.")

    if academic_year.status == AcademicYear.Status.CLOSED:
        raise ValidationError(f"El año lectivo {academic_year.year} ya se encuentra cerrado definitivamente.")

    enrollments = Enrollment.objects.filter(
        academic_year=academic_year,
        status=Enrollment.Status.ACTIVE
    ).select_related('student__user', 'course_section')

    total_evaluated = 0
    total_promoted = 0
    total_failed = 0

    for enr in enrollments:
        eval_result = evaluate_student_promotion(enr.student, enr.course_section, academic_year)
        enr.status = eval_result['status']
        enr.save()

        total_evaluated += 1
        if eval_result['is_promoted']:
            total_promoted += 1
        else:
            total_failed += 1

    # Bloquear todos los periodos del año
    AcademicPeriod.objects.filter(academic_year=academic_year).update(status=AcademicPeriod.Status.LOCKED)

    # Cerrar año lectivo
    academic_year.status = AcademicYear.Status.CLOSED
    academic_year.is_current = False
    academic_year.save()

    # Log de cierre formal
    log_entry = AcademicClosingLog.objects.create(
        academic_year=academic_year,
        closing_type=AcademicClosingLog.ClosingType.YEAR,
        closed_by=user,
        total_students_evaluated=total_evaluated,
        total_promoted=total_promoted,
        total_failed=total_failed,
        observations=observations
    )

    log_audit(
        action='UPDATE',
        table_name='AcademicYear',
        record_id=academic_year.id,
        old_values={'status': 'ACTIVE', 'is_current': True},
        new_values={'status': 'CLOSED', 'is_current': False},
        reason=f"CIERRE DEFINITIVO DE AÑO LECTIVO {academic_year.year}: {total_promoted} promovidos, {total_failed} no promovidos. {observations}",
        user=user
    )

    return {
        'total_evaluated': total_evaluated,
        'total_promoted': total_promoted,
        'total_failed': total_failed,
        'closing_log': log_entry,
    }
