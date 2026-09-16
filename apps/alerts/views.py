from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from .services import get_active_alerts_for_user
from .models import SystemAlert

@login_required
def active_alerts_partial(request):
    """
    Retorna el fragmento HTML con las alertas activas del usuario (para consumo HTMX).
    """
    alerts = get_active_alerts_for_user(request.user)
    return render(request, 'alerts/partials/alert_list.html', {'alerts': alerts})

@login_required
def dismiss_alert(request, alert_id):
    """
    Descarta una alerta permitida para el usuario actual.
    """
    alert = get_object_or_404(SystemAlert, id=alert_id, is_active=True)
    if alert.is_dismissible and alert.level != SystemAlert.Level.BLOCK:
        alert.is_active = False
        alert.save(update_fields=['is_active'])

    # Retorna lista actualizada
    alerts = get_active_alerts_for_user(request.user)
    return render(request, 'alerts/partials/alert_list.html', {'alerts': alerts})

@login_required
def activities_list_view(request):
    """
    Agenda de actividades institucionales del colegio.
    Permite a Directivos y Secretaría programar eventos y notificar a los alumnos.
    """
    from .models import InstitutionalActivity
    from .services import schedule_institutional_activity
    from django.contrib import messages
    from datetime import date

    if request.method == 'POST' and (request.user.is_admin_role or request.user.is_rector or request.user.is_secretary):
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        event_date_str = request.POST.get('event_date')
        event_time_str = request.POST.get('event_time')
        location = request.POST.get('location', '').strip() or 'Instalaciones del Colegio'
        target_audience = request.POST.get('target_audience', 'ALL')

        if title and event_date_str:
            try:
                from datetime import datetime
                event_date = datetime.strptime(event_date_str, '%Y-%m-%d').date()
                event_time = datetime.strptime(event_time_str, '%H:%M').time() if event_time_str else None

                activity = schedule_institutional_activity(
                    title=title,
                    description=description,
                    event_date=event_date,
                    event_time=event_time,
                    location=location,
                    target_audience=target_audience,
                    created_by=request.user
                )
                messages.success(request, f'Actividad "{title}" programada y notificada a los estudiantes con éxito.')
            except Exception as e:
                messages.error(request, f'Error al programar actividad: {str(e)}')
        else:
            messages.warning(request, 'Por favor ingrese el título y la fecha de la actividad.')

    # Listar actividades vigentes
    activities = InstitutionalActivity.objects.filter(is_active=True).order_by('event_date', 'event_time')
    
    # Filtrar según audiencia si es estudiante
    if request.user.is_student:
        activities = activities.filter(target_audience__in=['ALL', 'STUDENTS'])
    elif request.user.is_teacher:
        activities = activities.filter(target_audience__in=['ALL', 'TEACHERS'])
    elif request.user.is_parent:
        activities = activities.filter(target_audience__in=['ALL', 'PARENTS'])

    context = {
        'activities': activities,
        'today': date.today(),
        'can_schedule': request.user.is_admin_role or request.user.is_rector or request.user.is_secretary,
    }
    return render(request, 'alerts/activities_list.html', context)

