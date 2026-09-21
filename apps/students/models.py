from django.db import models
from django.conf import settings

class StudentProfile(models.Model):
    """
    Expediente escolar único del estudiante.
    Vincula su usuario de acceso con acudiente, código de matrícula y ficha médica.
    """
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile',
        limit_choices_to={'role': 'STUDENT'},
        verbose_name='Usuario Institucional'
    )
    student_code = models.CharField(
        max_length=30,
        unique=True,
        db_index=True,
        verbose_name='Código Estudiantil / Folio'
    )
    blood_type = models.CharField(
        max_length=5,
        default='O+',
        verbose_name='Grupo y Factor RH'
    )
    parent = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='dependent_students',
        limit_choices_to={'role': 'PARENT'},
        verbose_name='Padre de Familia / Acudiente'
    )
    eps = models.CharField(
        max_length=80,
        blank=True,
        null=True,
        verbose_name='Entidad Promotora de Salud (EPS)'
    )
    medical_notes = models.TextField(
        blank=True,
        null=True,
        verbose_name='Observaciones Médicas / Alergias'
    )

    class Meta:
        verbose_name = 'Expediente Estudiantil'
        verbose_name_plural = 'Expedientes Estudiantiles'
        ordering = ['user__last_name', 'user__first_name']

    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username} (Cód: {self.student_code})"

    @property
    def current_enrollment(self):
        """Retorna la matrícula activa en el año lectivo vigente."""
        return self.enrollments.filter(status=Enrollment.Status.ACTIVE, academic_year__is_current=True).first()


class Enrollment(models.Model):
    """
    Matrícula escolar: Vincula formalmente a un estudiante con un grupo/curso específico para un año lectivo.
    Restricción estricta: Un estudiante solo puede tener una matrícula activa por año escolar.
    """
    class Status(models.TextChoices):
        PENDING = 'PENDING', '🟡 Pendiente de Aprobación'
        ACTIVE = 'ACTIVE', '🟢 Matriculado / Activo'
        TRANSFERRED = 'TRANSFERRED', '🔵 Trasladado de Grupo'
        WITHDRAWN = 'WITHDRAWN', '🔴 Retirado / Desertor'
        PROMOTED = 'PROMOTED', '🎓 Promovido de Grado'
        FAILED = 'FAILED', '❌ No Promovido'

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Estudiante'
    )
    course_section = models.ForeignKey(
        'courses.CourseSection',
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Grupo / Sección'
    )
    academic_year = models.ForeignKey(
        'courses.AcademicYear',
        on_delete=models.CASCADE,
        related_name='enrollments',
        verbose_name='Año Lectivo'
    )
    enrollment_date = models.DateField(auto_now_add=True, verbose_name='Fecha de Matrícula')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
        db_index=True,
        verbose_name='Estado de Matrícula'
    )

    FINANCIAL_STATUS_CHOICES = [
        ('PAZ_Y_SALVO', '🟢 Paz y Salvo'),
        ('PENDIENTE', '🟡 Pendiente de Pago'),
        ('MORA', '🔴 En Mora'),
    ]
    financial_status = models.CharField(
        max_length=20,
        choices=FINANCIAL_STATUS_CHOICES,
        default='PAZ_Y_SALVO',
        verbose_name='Estado Financiero / Tesorería'
    )
    admission_requirement_info = models.CharField(
        max_length=150,
        blank=True,
        default='Requisitos de Admisión al día',
        verbose_name='Requisito de Admisión (Saber 11 / Prueba Aptitud / Paz y Salvo)'
    )

    class Meta:
        verbose_name = 'Matrícula Escolar'
        verbose_name_plural = 'Matrículas Escolares'
        unique_together = ('student', 'academic_year')
        ordering = ['course_section__grade_level__order', 'student__user__last_name']

    def __str__(self):
        return f"{self.student.user.get_full_name() or self.student.user.username} -> {self.course_section.name} ({self.academic_year.year})"


class StudentObservation(models.Model):
    """
    Observador del Estudiante / Bitácora de Seguimiento Convivencial y Académico.
    Permite registrar anotaciones, llamados de atención, compromisos y reconocimientos
    por parte de: Rector, Secretaría y Docentes.
    Visible para acudientes y alumnos en modo solo lectura.
    """
    class Category(models.TextChoices):
        ACADEMIC = 'ACADEMIC', '📚 Seguimiento Académico'
        DISCIPLINARY = 'DISCIPLINARY', '⚠️ Convivencial / Disciplinario'
        ATTENDANCE = 'ATTENDANCE', '⏰ Asistencia / Puntualidad'
        CITATION = 'CITATION', '📢 Citación a Acudiente'
        RECOGNITION = 'RECOGNITION', '⭐ Felicitación / Mérito'

    class Severity(models.TextChoices):
        INFO = 'INFO', 'Informativa / Positiva'
        WARNING = 'WARNING', 'Llamado de Atención'
        CRITICAL = 'CRITICAL', 'Falta Grave / Citación Urgente'

    student = models.ForeignKey(
        StudentProfile,
        on_delete=models.CASCADE,
        related_name='observations',
        verbose_name='Estudiante'
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name='authored_observations',
        verbose_name='Registrado por'
    )
    academic_year = models.ForeignKey(
        'courses.AcademicYear',
        on_delete=models.CASCADE,
        related_name='student_observations',
        verbose_name='Año Lectivo'
    )
    academic_period = models.ForeignKey(
        'periods.AcademicPeriod',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='student_observations',
        verbose_name='Periodo Lectivo'
    )
    category = models.CharField(
        max_length=25,
        choices=Category.choices,
        default=Category.ACADEMIC,
        verbose_name='Categoría'
    )
    severity = models.CharField(
        max_length=15,
        choices=Severity.choices,
        default=Severity.INFO,
        verbose_name='Nivel / Severidad'
    )
    title = models.CharField(max_length=150, verbose_name='Título de la Observación')
    description = models.TextField(verbose_name='Descripción de los Hechos')
    commitments = models.TextField(
        blank=True,
        null=True,
        verbose_name='Compromisos del Estudiante / Acuerdos'
    )
    parent_notified = models.BooleanField(
        default=False,
        verbose_name='¿Acudiente Notificado?'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Registro')

    class Meta:
        verbose_name = 'Observación de Estudiante'
        verbose_name_plural = 'Observador de Estudiantes'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} - {self.student.user.get_full_name()} ({self.get_category_display()})"

    @property
    def badge_class(self):
        mapping = {
            self.Severity.INFO: 'bg-info-subtle text-info-emphasis border-info-subtle',
            self.Severity.WARNING: 'bg-warning-subtle text-warning-emphasis border-warning-subtle',
            self.Severity.CRITICAL: 'bg-danger-subtle text-danger-emphasis border-danger-subtle',
        }
        return mapping.get(self.severity, 'bg-secondary text-white')

