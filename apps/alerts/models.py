from django.db import models
from django.conf import settings

class SystemAlert(models.Model):
    """
    Entidad base de semaforización y alertas institucionales de ACADEMIX.
    🔴 Bloqueo: No descartable, detiene acciones críticas.
    🟡 Advertencia: Indicador preventivo.
    🔵 Información: Datos y avisos complementarios.
    """
    class Level(models.TextChoices):
        BLOCK = 'BLOCK', '🔴 Bloqueo Crítico'
        WARNING = 'WARNING', '🟡 Advertencia'
        INFO = 'INFO', '🔵 Información'

    title = models.CharField(max_length=150, verbose_name='Título')
    message = models.TextField(verbose_name='Mensaje descriptivo')
    level = models.CharField(
        max_length=15,
        choices=Level.choices,
        default=Level.INFO,
        db_index=True,
        verbose_name='Nivel de Alerta'
    )
    recipient_user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='personal_alerts',
        verbose_name='Usuario Destinatario'
    )
    target_role = models.CharField(
        max_length=20,
        blank=True,
        null=True,
        verbose_name='Rol Destinatario (Opcional)'
    )
    is_dismissible = models.BooleanField(
        default=True,
        verbose_name='¿Es Descartable?'
    )
    is_active = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name='¿Está Activa?'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Emisión')

    class Meta:
        verbose_name = 'Alerta del Sistema'
        verbose_name_plural = 'Alertas del Sistema'
        ordering = ['-created_at']

    def __str__(self):
        return f"[{self.get_level_display()}] {self.title}"

    @property
    def bootstrap_alert_class(self):
        """Retorna la clase CSS de Bootstrap 5 según el nivel de semáforo."""
        mapping = {
            self.Level.BLOCK: 'alert-danger border-danger shadow-sm',
            self.Level.WARNING: 'alert-warning border-warning shadow-sm',
            self.Level.INFO: 'alert-info border-info shadow-sm',
        }
        return mapping.get(self.level, 'alert-secondary')

    @property
    def badge_class(self):
        mapping = {
            self.Level.BLOCK: 'bg-danger text-white',
            self.Level.WARNING: 'bg-warning text-dark',
            self.Level.INFO: 'bg-primary text-white',
        }
        return mapping.get(self.level, 'bg-secondary text-white')


class InstitutionalActivity(models.Model):
    """
    Actividad o evento programado en la institución (académica, cultural, deportiva).
    Despacha notificaciones a los estudiantes y la comunidad educativa.
    """
    class TargetAudience(models.TextChoices):
        ALL = 'ALL', 'Toda la Comunidad'
        STUDENTS = 'STUDENTS', 'Solo Estudiantes'
        TEACHERS = 'TEACHERS', 'Solo Docentes'
        PARENTS = 'PARENTS', 'Solo Padres y Acudientes'

    title = models.CharField(max_length=160, verbose_name='Título de la Actividad')
    description = models.TextField(verbose_name='Descripción de la Actividad')
    event_date = models.DateField(verbose_name='Fecha de la Actividad')
    event_time = models.TimeField(null=True, blank=True, verbose_name='Hora de la Actividad')
    location = models.CharField(max_length=120, default='Instalaciones del Colegio', verbose_name='Lugar / Espacio')
    target_audience = models.CharField(
        max_length=20,
        choices=TargetAudience.choices,
        default=TargetAudience.ALL,
        verbose_name='Dirigido a'
    )
    is_active = models.BooleanField(default=True, verbose_name='¿Actividad Vigente?')
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='created_activities',
        verbose_name='Programado por'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Actividad Institucional'
        verbose_name_plural = 'Actividades Institucionales'
        ordering = ['event_date', 'event_time']

    def __str__(self):
        return f"{self.title} ({self.event_date})"

