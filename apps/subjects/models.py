from decimal import Decimal
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class KnowledgeArea(models.Model):
    """
    Área Fundamental u Optativa de Conocimiento (ej. Matemáticas, Ciencias Naturales).
    """
    name = models.CharField(max_length=100, unique=True, verbose_name='Nombre del Área')
    order = models.PositiveSmallIntegerField(default=1, verbose_name='Orden en Boletines')

    class Meta:
        verbose_name = 'Área de Conocimiento'
        verbose_name_plural = 'Áreas de Conocimiento'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name


class Subject(models.Model):
    """
    Asignatura individual (ej. Álgebra, Biología, Filosofía, Inglés).
    """
    area = models.ForeignKey(
        KnowledgeArea,
        on_delete=models.PROTECT,
        related_name='subjects',
        verbose_name='Área Fundamental'
    )
    name = models.CharField(max_length=100, verbose_name='Nombre de la Asignatura')
    code = models.CharField(max_length=20, unique=True, verbose_name='Código Abreviado')
    description = models.TextField(blank=True, null=True, verbose_name='Descripción Curricular')

    class Meta:
        verbose_name = 'Asignatura'
        verbose_name_plural = 'Asignaturas'
        ordering = ['area', 'name']

    def __str__(self):
        return f"{self.name} ({self.code})"


class GradeSubject(models.Model):
    """
    Malla Curricular: Configuración de Asignatura para un Grado Escolar específico.
    Define la intensidad horaria semanal y el peso porcentual dentro del área.
    """
    grade_level = models.ForeignKey(
        'courses.GradeLevel',
        on_delete=models.CASCADE,
        related_name='curriculum_subjects',
        verbose_name='Grado Escolar'
    )
    subject = models.ForeignKey(
        Subject,
        on_delete=models.CASCADE,
        related_name='curriculum_grades',
        verbose_name='Asignatura'
    )
    weekly_hours = models.PositiveSmallIntegerField(
        default=4,
        validators=[MinValueValidator(1), MaxValueValidator(20)],
        verbose_name='Horas Semanales (Intensidad)'
    )
    weight_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal('100.00'),
        validators=[MinValueValidator(Decimal('0.01')), MaxValueValidator(Decimal('100.00'))],
        verbose_name='Peso en el Área (%)'
    )

    class Meta:
        verbose_name = 'Asignatura en Malla Curricular'
        verbose_name_plural = 'Malla Curricular por Grado'
        unique_together = ('grade_level', 'subject')
        ordering = ['grade_level__order', 'subject__area__order', 'subject__name']

    def __str__(self):
        return f"{self.subject.name} - Grado {self.grade_level.name} ({self.weekly_hours}h/sem)"
