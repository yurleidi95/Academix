from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import HttpResponse
from .models import PromotionRule, AcademicClosingLog
from .services import (
    get_or_create_promotion_rule,
    close_academic_period,
    reopen_academic_period,
    execute_annual_closing,
    evaluate_student_promotion
)
from apps.periods.models import AcademicPeriod
from apps.courses.models import AcademicYear, CourseSection
from apps.courses.services import get_current_academic_year
from apps.students.models import StudentProfile, Enrollment

def is_admin_or_rector(user):
    return user.is_authenticated and (user.is_admin_role or user.is_rector)

@login_required
@user_passes_test(is_admin_or_rector)
def closing_manager_view(request):
    """
    Panel directivo para supervisión y gestión de cierres de periodos y año escolar.
    """
    current_year = get_current_academic_year()
    periods = AcademicPeriod.objects.filter(academic_year=current_year).order_by('number') if current_year else []
    rule = get_or_create_promotion_rule(current_year) if current_year else None
    logs = AcademicClosingLog.objects.filter(academic_year=current_year).select_related('closed_by')[:10] if current_year else []

    # Estadísticas preliminares de matrículas activas
    total_active_students = Enrollment.objects.filter(
        academic_year=current_year,
        status=Enrollment.Status.ACTIVE
    ).count() if current_year else 0

    context = {
        'current_year': current_year,
        'periods': periods,
        'rule': rule,
        'logs': logs,
        'total_active_students': total_active_students,
    }
    return render(request, 'rules/closing_manager.html', context)

@login_required
@user_passes_test(is_admin_or_rector)
def close_period_view(request, period_id):
    """
    Cierra formalmente un periodo lectivo configurando la autorización de firma de rectoría.
    """
    if request.method == 'POST':
        period = get_object_or_404(AcademicPeriod, id=period_id)
        reason = request.POST.get('reason', 'Cierre formal de periodo lectivo')
        rector_sig_raw = request.POST.get('rector_signature_authorized', 'true')
        rector_signature_authorized = (str(rector_sig_raw).lower() in ['true', '1', 'on', 'yes', 'si', 'sí'])
        try:
            close_academic_period(period, request.user, reason, rector_signature_authorized=rector_signature_authorized)
            sig_msg = "con Firma Digital de Rectora autorizada" if rector_signature_authorized else "sin firma digital (espacio para rúbrica manual)"
            messages.success(request, f'El periodo {period.name} ha sido cerrado ({sig_msg}). Se ha bloqueado la alteración de notas.')
        except Exception as e:
            messages.error(request, f'Error al cerrar periodo: {str(e)}')
    return redirect('rules:closing_manager')

@login_required
@user_passes_test(is_admin_or_rector)
def reopen_period_view(request, period_id):
    """
    Reabre extraordinariamente un periodo cerrado con justificación requerida.
    """
    if request.method == 'POST':
        period = get_object_or_404(AcademicPeriod, id=period_id)
        reason = request.POST.get('reason', '').strip()
        try:
            reopen_academic_period(period, request.user, reason)
            messages.warning(request, f'El periodo {period.name} ha sido reabierto. La acción ha sido registrada en auditoría inmutable.')
        except Exception as e:
            messages.error(request, f'Error al reabrir periodo: {str(e)}')
    return redirect('rules:closing_manager')

@login_required
@user_passes_test(is_admin_or_rector)
def execute_year_closing_view(request, year_id):
    """
    Ejecuta el cierre anual definitivo del año lectivo y la promoción escolar.
    """
    if request.method == 'POST':
        academic_year = get_object_or_404(AcademicYear, id=year_id)
        observations = request.POST.get('observations', '').strip()
        try:
            result = execute_annual_closing(academic_year, request.user, observations)
            messages.success(
                request,
                f'¡Cierre definitivo completado! Se evaluaron {result["total_evaluated"]} estudiantes: '
                f'{result["total_promoted"]} promovidos y {result["total_failed"]} no promovidos.'
            )
        except Exception as e:
            messages.error(request, f'Error durante el cierre anual: {str(e)}')
    return redirect('rules:closing_manager')
