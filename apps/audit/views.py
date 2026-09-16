from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.db.models import Q
from .models import AuditLog

def is_admin_or_rector(user):
    return user.is_authenticated and (user.is_admin_role or user.is_rector)

@login_required
@user_passes_test(is_admin_or_rector)
def audit_list_view(request):
    """
    Visor de auditoría inmutable para directivos y administradores.
    Soporta filtrado reactivo vía HTMX por acción, tabla o término de búsqueda.
    """
    query = request.GET.get('q', '').strip()
    action_filter = request.GET.get('action', '').strip()
    table_filter = request.GET.get('table', '').strip()

    logs = AuditLog.objects.select_related('user').all()

    if query:
        logs = logs.filter(
            Q(reason__icontains=query) |
            Q(user__username__icontains=query) |
            Q(user__first_name__icontains=query) |
            Q(user__last_name__icontains=query) |
            Q(record_id__icontains=query)
        )
    if action_filter:
        logs = logs.filter(action=action_filter)
    if table_filter:
        logs = logs.filter(table_name__icontains=table_filter)

    paginator = Paginator(logs, 25)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'actions': AuditLog.Action.choices,
        'query': query,
        'action_filter': action_filter,
        'table_filter': table_filter,
    }

    if request.headers.get('HX-Request'):
        return render(request, 'audit/partials/audit_table.html', context)

    return render(request, 'audit/list.html', context)

@login_required
@user_passes_test(is_admin_or_rector)
def export_audit_csv_view(request):
    """
    Exportación de la bitácora inmutable de auditoría a CSV para análisis forense externo.
    """
    import csv, io
    from django.http import HttpResponse

    logs = AuditLog.objects.select_related('user').order_by('-id')

    output = io.StringIO()
    output.write('\ufeff')
    writer = csv.writer(output, dialect='excel')
    writer.writerow([
        'ID', 'Fecha y Hora', 'Usuario', 'Rol', 'Acción',
        'Tabla Afectada', 'ID Registro', 'IP Origen', 'Motivo / Justificación',
        'Datos Anteriores (JSON)', 'Datos Nuevos (JSON)'
    ])

    for log in logs:
        writer.writerow([
            log.id,
            log.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            log.user.username if log.user else 'Sistema / Anónimo',
            log.user.get_role_display() if log.user else '-',
            log.get_action_display(),
            log.table_name,
            log.record_id or '',
            log.ip_address or '',
            log.reason,
            str(log.old_values or ''),
            str(log.new_values or '')
        ])

    response = HttpResponse(output.getvalue(), content_type='text/csv; charset=utf-8')
    response['Content-Disposition'] = 'attachment; filename="Auditoria_Forense_Academix.csv"'
    return response

@login_required
@user_passes_test(is_admin_or_rector)
def audit_detail_modal_view(request, log_id):
    """
    Modal para visualización detallada y comparación de diferencias (old vs new) de un registro auditable.
    """
    from django.shortcuts import get_object_or_404
    log = get_object_or_404(AuditLog.objects.select_related('user'), id=log_id)
    return render(request, 'audit/partials/detail_modal.html', {'log': log})

