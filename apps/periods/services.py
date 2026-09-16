from decimal import Decimal
from datetime import timedelta
from django.db import transaction
from .models import AcademicPeriod
from apps.audit.services import log_audit

def get_current_active_period(academic_year):
    """Retorna el periodo activo actual dentro del año lectivo."""
    return AcademicPeriod.objects.filter(academic_year=academic_year, status=AcademicPeriod.Status.ACTIVE).first()

@transaction.atomic
def change_period_status(period_id, new_status, reason, user=None):
    """
    Cambia el estado de un periodo (ej. Activo -> Cerrado o Bloqueado)
    con auditoría estricta y validación de permisos.
    """
    period = AcademicPeriod.objects.select_for_update().get(id=period_id)
    old_status = period.status
    
    period.status = new_status
    period.save(update_fields=['status'])

    action = 'PERIOD_CLOSE' if new_status in [AcademicPeriod.Status.CLOSED, AcademicPeriod.Status.LOCKED] else 'UPDATE'
    log_audit(
        action=action,
        table_name='AcademicPeriod',
        record_id=period.id,
        old_values={'status': old_status},
        new_values={'status': new_status},
        reason=reason or f'Cambio de estado de periodo {period.name} a {new_status}',
        user=user
    )

    return period

@transaction.atomic
def create_standard_periods(academic_year, user=None):
    """
    Inicializa los 4 periodos estándar (25% cada uno) para un año escolar.
    """
    created_periods = []
    total_days = (academic_year.end_date - academic_year.start_date).days
    period_days = total_days // 4

    for i in range(1, 5):
        p_start = academic_year.start_date + timedelta(days=(i - 1) * period_days)
        p_end = academic_year.start_date + timedelta(days=i * period_days - 1) if i < 4 else academic_year.end_date

        period, created = AcademicPeriod.objects.get_or_create(
            academic_year=academic_year,
            number=i,
            defaults={
                'name': f'Periodo {i}',
                'start_date': p_start,
                'end_date': p_end,
                'percentage': Decimal('25.00'),
                'status': AcademicPeriod.Status.ACTIVE if i == 1 else AcademicPeriod.Status.CLOSED
            }
        )
        created_periods.append(period)

    return created_periods
