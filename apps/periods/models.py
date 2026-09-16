from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class AcademicPeriod(models.Model):
    """
    Periodo Académico o Corte Escolar (ej. Periodo 1, 2, 3 o 4).
    Controla los plazos de edición y los estados:
    - ACTIVE: Abierto para registro de notas y asistencia.
    - CLOSED: Concluido, pendiente de aprobación o cierre definitivo.
    - LOCKED: Bloqueado contra modificaciones (solo rector/admin con justificación).
    """
    class Status(models.TextChoices):
        ACTIVE = 'ACTIVE', '🟢 Abierto / Activo'
        CLOSED = 'CLOSED', '🟡 Cerrado'
        LOCKED = 'LOCKED', '🔴 Bloqueado'

    academic_year = models.ForeignKey(
        'courses.AcademicYear',
        on_delete=models.CASCADE,
        related_name='periods',
        verbose_name='Año Lectivo'
    )
    number = models.PositiveSmallIntegerField(verbose_name='Número de Periodo (1-4)')
    name = models.CharField(max_length=60, verbose_name='Nombre del Periodo')
    start_date = models.DateField(verbose_name='Fecha de Inicio')
    end_date = models.DateField(verbose_name='Fecha de Finalización')
    percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('25.00'),
        validators=[MinValueValidator(Decimal('0.01')), MaxValueValidator(Decimal('100.00'))],
        verbose_name='Ponderación Anual (%)'
    )
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.ACTIVE,
        db_index=True,
        verbose_name='Estado del Periodo'
    )

    class Meta:
        verbose_name = 'Periodo Académico'
        verbose_name_plural = 'Periodos Académicos'
        unique_together = ('academic_year', 'number')
        ordering = ['academic_year', 'number']

    def __str__(self):
        return f"{self.name} - {self.academic_year.year} ({self.get_status_display()})"

    @property
    def is_editable(self):
        return self.status == self.Status.ACTIVE

    @property
    def status_badge_class(self):
        mapping = {
            self.Status.ACTIVE: 'bg-success text-white',
            self.Status.CLOSED: 'bg-warning text-dark',
            self.Status.LOCKED: 'bg-danger text-white',
        }
        return mapping.get(self.status, 'bg-secondary text-white')
