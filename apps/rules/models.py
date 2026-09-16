from decimal import Decimal
from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class PromotionRule(models.Model):
    """
    Reglas institucionales de evaluación y promoción escolar bajo el Decreto 1290.
    Configura umbrales de reprobación, notas mínimas y ausentismo máximo.
    """
    academic_year = models.OneToOneField(
        'courses.AcademicYear',
        on_delete=models.CASCADE,
        related_name='promotion_rule',
        verbose_name='Año Lectivo'
    )
    min_passing_grade = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        default=Decimal('3.00'),
        validators=[MinValueValidator(Decimal('1.00')), MaxValueValidator(Decimal('5.00'))],
        verbose_name='Calificación Mínima Aprobatoria'
    )
    max_failed_subjects = models.PositiveSmallIntegerField(
        default=2,
        verbose_name='Máximo de Asignaturas Reprobadas Permitidas'
    )
    max_absence_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('20.00'),
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('100.00'))],
        verbose_name='Porcentaje Máximo de Inasistencias (%)'
    )
    is_active = models.BooleanField(default=True, verbose_name='Regla Activa')
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Regla de Promoción'
        verbose_name_plural = 'Reglas de Promoción'

    def __str__(self):
        return f"Regla Promoción {self.academic_year.year} (Mín: {self.min_passing_grade}, Max Faltas: {self.max_absence_percentage}%)"


class AnnualFinalGrade(models.Model):
    """
    Calificación definitiva consolidada anual de un estudiante en una asignatura específica.
    Pondera los periodos lectivos cursados y determina la aprobación de la materia.
    """
    class PerformanceLevel(models.TextChoices):
        BAJO = 'BAJO', 'Bajo (1.00 - 2.99)'
        BASICO = 'BASICO', 'Básico (3.00 - 3.99)'
        ALTO = 'ALTO', 'Alto (4.00 - 4.59)'
        SUPERIOR = 'SUPERIOR', 'Superior (4.60 - 5.00)'

    student = models.ForeignKey(
        'students.StudentProfile',
        on_delete=models.CASCADE,
        related_name='annual_grades',
        verbose_name='Estudiante'
    )
    course_section = models.ForeignKey(
        'courses.CourseSection',
        on_delete=models.CASCADE,
        related_name='annual_grades',
        verbose_name='Grupo / Sección'
    )
    subject = models.ForeignKey(
        'subjects.Subject',
        on_delete=models.CASCADE,
        related_name='annual_grades',
        verbose_name='Asignatura'
    )
    academic_year = models.ForeignKey(
        'courses.AcademicYear',
        on_delete=models.CASCADE,
        related_name='annual_grades',
        verbose_name='Año Lectivo'
    )
    final_score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('1.00')), MaxValueValidator(Decimal('5.00'))],
        verbose_name='Calificación Definitiva Anual'
    )
    performance_level = models.CharField(
        max_length=15,
        choices=PerformanceLevel.choices,
        default=PerformanceLevel.BAJO,
        verbose_name='Nivel de Desempeño'
    )
    is_approved = models.BooleanField(default=True, verbose_name='¿Asignatura Aprobada?')
    recalculated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Definitiva Anual'
        verbose_name_plural = 'Definitivas Anuales'
        unique_together = ('student', 'course_section', 'subject', 'academic_year')
        ordering = ['student', 'subject']

    def __str__(self):
        return f"{self.student.user.username} - {self.subject.code}: {self.final_score} ({self.get_performance_level_display()})"

    @property
    def badge_class(self):
        mapping = {
            self.PerformanceLevel.BAJO: 'bg-danger text-white',
            self.PerformanceLevel.BASICO: 'bg-warning text-dark',
            self.PerformanceLevel.ALTO: 'bg-primary text-white',
            self.PerformanceLevel.SUPERIOR: 'bg-success text-white',
        }
        return mapping.get(self.performance_level, 'bg-secondary text-white')


class AcademicClosingLog(models.Model):
    """
    Trazabilidad y registro formal de los cierres de periodo lectivo o de año escolar completo.
    """
    class ClosingType(models.TextChoices):
        PERIOD = 'PERIOD', 'Cierre de Periodo Lectivo'
        YEAR = 'YEAR', 'Cierre Definitivo de Año Escolar'

    academic_year = models.ForeignKey(
        'courses.AcademicYear',
        on_delete=models.CASCADE,
        related_name='closing_logs',
        verbose_name='Año Lectivo'
    )
    academic_period = models.ForeignKey(
        'periods.AcademicPeriod',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='closing_logs',
        verbose_name='Periodo Lectivo'
    )
    closing_type = models.CharField(
        max_length=10,
        choices=ClosingType.choices,
        default=ClosingType.PERIOD,
        verbose_name='Tipo de Cierre'
    )
    closed_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        verbose_name='Ejecutado por'
    )
    closed_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha y Hora de Cierre')
    total_students_evaluated = models.PositiveIntegerField(default=0, verbose_name='Total Estudiantes Evaluados')
    total_promoted = models.PositiveIntegerField(default=0, verbose_name='Total Promovidos')
    total_failed = models.PositiveIntegerField(default=0, verbose_name='Total No Promovidos')
    observations = models.TextField(blank=True, verbose_name='Observaciones / Justificación')

    class Meta:
        verbose_name = 'Bitácora de Cierre Académico'
        verbose_name_plural = 'Bitácoras de Cierre Académico'
        ordering = ['-closed_at']

    def __str__(self):
        target = self.academic_period.name if self.academic_period else f"Año {self.academic_year.year}"
        return f"{self.get_closing_type_display()} [{target}] por {self.closed_by.username} ({self.closed_at.strftime('%Y-%m-%d %H:%M')})"
