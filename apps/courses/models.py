from django.db import models
from django.conf import settings

class AcademicYear(models.Model):
    """
    Año Lectivo escolar (ej. 2026).
    Solo un año lectivo puede ser el año activo (is_current=True).
    """
    class Status(models.TextChoices):
        PLANNING = 'PLANNING', 'En Planificación'
        ACTIVE = 'ACTIVE', 'En Curso (Activo)'
        CLOSED = 'CLOSED', 'Cerrado / Concluido'

    year = models.PositiveSmallIntegerField(unique=True, verbose_name='Año Calendario')
    name = models.CharField(max_length=60, verbose_name='Nombre Descriptivo')
    start_date = models.DateField(verbose_name='Fecha de Inicio')
    end_date = models.DateField(verbose_name='Fecha de Finalización')
    status = models.CharField(
        max_length=15,
        choices=Status.choices,
        default=Status.PLANNING,
        db_index=True,
        verbose_name='Estado'
    )
    is_current = models.BooleanField(
        default=False,
        db_index=True,
        verbose_name='¿Es el Año Vigente Actual?'
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Año Lectivo'
        verbose_name_plural = 'Años Lectivos'
        ordering = ['-year']

    def __str__(self):
        current_badge = " [VIGENTE]" if self.is_current else ""
        return f"{self.name} ({self.get_status_display()}){current_badge}"


class GradeLevel(models.Model):
    """
    Grado Escolar (ej. Sexto, Séptimo, Décimo, Once).
    """
    class LevelStage(models.TextChoices):
        PRIMARIA = 'PRIMARIA', 'Básica Primaria'
        SECUNDARIA = 'SECUNDARIA', 'Básica Secundaria'
        MEDIA = 'MEDIA', 'Educación Media'

    name = models.CharField(max_length=50, verbose_name='Nombre del Grado')
    code = models.CharField(max_length=10, unique=True, verbose_name='Código de Grado')
    level_stage = models.CharField(
        max_length=20,
        choices=LevelStage.choices,
        default=LevelStage.SECUNDARIA,
        verbose_name='Nivel Académico'
    )
    order = models.PositiveSmallIntegerField(default=1, verbose_name='Orden Numérico')

    class Meta:
        verbose_name = 'Grado Escolar'
        verbose_name_plural = 'Grados Escolares'
        ordering = ['order']

    def __str__(self):
        return f"{self.name} ({self.get_level_stage_display()})"


class CourseSection(models.Model):
    """
    Curso, Grupo o Sección Escolar (ej. 6-A, 10-1) dentro de un año lectivo.
    """
    academic_year = models.ForeignKey(
        AcademicYear,
        on_delete=models.PROTECT,
        related_name='sections',
        verbose_name='Año Lectivo'
    )
    grade_level = models.ForeignKey(
        GradeLevel,
        on_delete=models.PROTECT,
        related_name='sections',
        verbose_name='Grado Escolar'
    )
    name = models.CharField(max_length=25, verbose_name='Identificador del Grupo (ej. 6-A)')
    classroom = models.CharField(max_length=50, blank=True, null=True, verbose_name='Aula Asignada')
    homeroom_teacher = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='homeroom_sections',
        limit_choices_to={'role': 'TEACHER'},
        verbose_name='Director de Grupo'
    )
    capacity = models.PositiveSmallIntegerField(default=35, verbose_name='Cupo Máximo')
    is_active = models.BooleanField(default=True, verbose_name='¿Grupo Activo?')

    class Meta:
        verbose_name = 'Curso / Grupo'
        verbose_name_plural = 'Cursos / Grupos'
        unique_together = ('academic_year', 'grade_level', 'name')
        ordering = ['academic_year', 'grade_level__order', 'name']

    def __str__(self):
        return f"{self.name} - {self.academic_year.year}"

    @property
    def enrolled_count(self):
        return self.enrollments.filter(status='ACTIVE').count()
