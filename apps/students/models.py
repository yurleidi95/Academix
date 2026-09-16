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

    class Meta:
        verbose_name = 'Matrícula Escolar'
        verbose_name_plural = 'Matrículas Escolares'
        unique_together = ('student', 'academic_year')
        ordering = ['course_section__grade_level__order', 'student__user__last_name']

    def __str__(self):
        return f"{self.student.user.get_full_name() or self.student.user.username} -> {self.course_section.name} ({self.academic_year.year})"
