import threading

_thread_locals = threading.local()

def get_current_user():
    """Retorna el usuario actual almacenado en el hilo de ejecución."""
    return getattr(_thread_locals, 'user', None)

def get_current_ip():
    """Retorna la IP actual almacenada en el hilo de ejecución."""
    return getattr(_thread_locals, 'ip', None)

def get_current_request():
    """Retorna el objeto request actual."""
    return getattr(_thread_locals, 'request', None)

class AuditMiddleware:
    """
    Middleware para capturar el usuario autenticado y la dirección IP
    del cliente en cada petición HTTP, facilitando la auditoría inmutable.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Extraer IP remota respetando proxies o cabeceras estándar
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0].strip()
        else:
            ip = request.META.get('REMOTE_ADDR')

        _thread_locals.user = getattr(request, 'user', None) if request.user.is_authenticated else None
        _thread_locals.ip = ip
        _thread_locals.request = request

        response = self.get_response(request)

        # Limpiar al finalizar el ciclo de la petición
        _thread_locals.user = None
        _thread_locals.ip = None
        _thread_locals.request = None

        return response
