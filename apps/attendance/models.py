from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

class AttendanceSession(models.Model):
    """
    Sesión de clase escolar para toma de asistencia.
    Agrupa la toma de asistencia de una fecha, curso, asignatura y periodo lectivo.
    """
    course_section = models.ForeignKey(
        'courses.CourseSection',
        on_delete=models.CASCADE,
        related_name='attendance_sessions',
        verbose_name='Curso / Grupo'
    )
    subject = models.ForeignKey(
        'subjects.Subject',
        on_delete=models.CASCADE,
        related_name='attendance_sessions',
        verbose_name='Asignatura'
    )
    academic_period = models.ForeignKey(
        'periods.AcademicPeriod',
        on_delete=models.CASCADE,
        related_name='attendance_sessions',
        verbose_name='Periodo Lectivo'
    )
    teaching_assignment = models.ForeignKey(
        'teachers.TeachingAssignment',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='attendance_sessions',
        verbose_name='Asignación Docente'
    )
    date = models.DateField(
        db_index=True,
        verbose_name='Fecha de la Clase'
    )
    hours_count = models.PositiveSmallIntegerField(
        default=1,
        verbose_name='Horas Pedagógicas Impartidas'
    )
    recorded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='recorded_attendances',
        verbose_name='Registrado por'
    )
    observations = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observaciones de la Jornada'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Sesión de Asistencia'
        verbose_name_plural = 'Sesiones de Asistencia'
        unique_together = ('course_section', 'subject', 'date', 'academic_period')
        ordering = ['-date', 'course_section', 'subject']

    def __str__(self):
        return f"{self.course_section.name} - {self.subject.code} ({self.date.strftime('%d/%m/%Y')})"

    def clean(self):
        """Valida que el periodo no esté cerrado ni bloqueado."""
        if self.academic_period and not self.academic_period.is_editable:
            raise ValidationError(f"No es posible registrar ni modificar asistencias en el periodo {self.academic_period.name} porque se encuentra {self.academic_period.get_status_display()}.")


class AttendanceRecord(models.Model):
    """
    Registro individual de asistencia de un estudiante en una sesión de clase.
    """
    class Status(models.TextChoices):
        PRESENT = 'PRESENT', '🟢 Presente'
        LATE = 'LATE', '⏱️ Tardanza'
        JUSTIFIED = 'JUSTIFIED', '📝 Falta Justificada'
        UNJUSTIFIED = 'UNJUSTIFIED', '❌ Falta Injustificada'

    session = models.ForeignKey(
        AttendanceSession,
        on_delete=models.CASCADE,
        related_name='records',
        verbose_name='Sesión de Asistencia'
    )
    student = models.ForeignKey(
        'students.StudentProfile',
        on_delete=models.CASCADE,
        related_name='attendance_records',
        verbose_name='Estudiante'
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PRESENT,
        db_index=True,
        verbose_name='Estado de Asistencia'
    )
    justification = models.TextField(
        blank=True,
        null=True,
        verbose_name='Motivo de Justificación / Soporte'
    )
    justification_file = models.FileField(
        upload_to='attendance_justifications/',
        blank=True,
        null=True,
        verbose_name='Comprobante Adjunto (Excusa Médica)'
    )
    is_justified = models.BooleanField(
        default=False,
        verbose_name='¿Inasistencia Justificada?'
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Registro de Asistencia'
        verbose_name_plural = 'Registros de Asistencia'
        unique_together = ('session', 'student')
        ordering = ['student__user__last_name', 'student__user__first_name']

    def __str__(self):
        return f"{self.student.user.last_name}: {self.get_status_display()}"

    def save(self, *args, **kwargs):
        # Sincronizar flag is_justified si el estado es JUSTIFIED
        if self.status == self.Status.JUSTIFIED:
            self.is_justified = True
        elif self.status == self.Status.UNJUSTIFIED:
            self.is_justified = False
        super().save(*args, **kwargs)

    @property
    def badge_class(self):
        mapping = {
            self.Status.PRESENT: 'bg-success text-white',
            self.Status.LATE: 'bg-warning text-dark',
            self.Status.JUSTIFIED: 'bg-info text-dark',
            self.Status.UNJUSTIFIED: 'bg-danger text-white',
        }
        return mapping.get(self.status, 'bg-secondary text-white')
