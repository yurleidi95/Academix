import json
from .models import AuditLog
from .middleware import get_current_user, get_current_ip

def serialize_for_audit(data):
    """
    Serializa estructuras de datos u objetos a formato amigable JSON para auditoría.
    """
    if data is None:
        return None
    if isinstance(data, dict):
        cleaned = {}
        for k, v in data.items():
            # Evitar registrar contraseñas o datos sensibles en texto plano
            if 'password' in k.lower() or 'secret' in k.lower():
                cleaned[k] = '***PROTEGIDO***'
            else:
                cleaned[k] = str(v) if not isinstance(v, (int, float, bool, str, type(None))) else v
        return cleaned
    return {'detail': str(data)}

def log_audit(
    action,
    table_name,
    record_id=None,
    old_values=None,
    new_values=None,
    reason=None,
    user=None,
    ip=None,
    request=None
):
    """
    Función de servicio centralizada para registrar eventos en la auditoría inmutable de ACADEMIX.
    """
    if user is None:
        user = get_current_user()

    if ip is None:
        if request:
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip = x_forwarded_for.split(',')[0].strip()
            else:
                ip = request.META.get('REMOTE_ADDR')
        else:
            ip = get_current_ip()

    serialized_old = serialize_for_audit(old_values)
    serialized_new = serialize_for_audit(new_values)

    return AuditLog.objects.create(
        user=user if (user and user.is_authenticated) else None,
        action=action,
        table_name=table_name,
        record_id=str(record_id) if record_id is not None else None,
        old_values=serialized_old,
        new_values=serialized_new,
        ip_address=ip,
        reason=reason
    )
