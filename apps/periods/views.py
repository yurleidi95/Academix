from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import AcademicPeriod
from .services import change_period_status
from apps.courses.services import get_current_academic_year

@login_required
def periods_list_view(request):
    """
    Vista de control y supervisión de periodos académicos.
    """
    current_year = get_current_academic_year()
    periods = AcademicPeriod.objects.filter(academic_year=current_year).order_by('number') if current_year else []

    context = {
        'current_year': current_year,
        'periods': periods,
    }
    return render(request, 'periods/list.html', context)

@login_required
def update_status_htmx(request, period_id):
    """
    Endpoint HTMX para cambiar el estado de un periodo lectivo (Activo / Cerrado / Bloqueado).
    Solo accesible para Administrador y Rector.
    """
    if not (request.user.is_admin_role or request.user.is_rector):
        messages.error(request, 'No tiene permisos para modificar estados de periodos.')
        return redirect('periods:list')

    period = get_object_or_404(AcademicPeriod, id=period_id)
    new_status = request.POST.get('status')
    reason = request.POST.get('reason', 'Cambio manual de estado desde interfaz directiva')

    if new_status in AcademicPeriod.Status.values:
        change_period_status(period.id, new_status, reason=reason, user=request.user)
        messages.success(request, f'Periodo {period.name} actualizado a {period.get_status_display()}.')

    current_year = period.academic_year
    periods = AcademicPeriod.objects.filter(academic_year=current_year).order_by('number')
    return render(request, 'periods/partials/periods_table.html', {'periods': periods, 'current_year': current_year})
