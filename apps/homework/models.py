from decimal import Decimal
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Homework(models.Model):
    """
    Tarea o Actividad Académica asignada por un docente a un grupo escolar.
    """
    course_section = models.ForeignKey(
        'courses.CourseSection',
        on_delete=models.CASCADE,
        related_name='homeworks',
        verbose_name='Curso / Sección'
    )
    subject = models.ForeignKey(
        'subjects.Subject',
        on_delete=models.CASCADE,
        related_name='homeworks',
        verbose_name='Asignatura'
    )
    academic_period = models.ForeignKey(
        'periods.AcademicPeriod',
        on_delete=models.CASCADE,
        related_name='homeworks',
        verbose_name='Periodo Lectivo'
    )
    teacher = models.ForeignKey(
        'teachers.TeacherProfile',
        on_delete=models.CASCADE,
        related_name='created_homeworks',
        verbose_name='Docente Asignador'
    )
    title = models.CharField(max_length=150, verbose_name='Título de la Actividad')
    description = models.TextField(verbose_name='Instrucciones y Requisitos')
    due_date = models.DateTimeField(verbose_name='Fecha y Hora Límite de Entrega')
    attachment = models.FileField(
        upload_to='homework_attachments/',
        blank=True,
        null=True,
        verbose_name='Guía o Material Adjunto (PDF/Doc)'
    )
    is_active = models.BooleanField(default=True, verbose_name='¿Habilitada?')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Tarea Escolar'
        verbose_name_plural = 'Tareas Escolares'
        ordering = ['-due_date']

    def __str__(self):
        return f"{self.title} - {self.course_section.name} ({self.subject.code})"

    @property
    def is_expired(self):
        return timezone.now() > self.due_date

    @property
    def submission_count(self):
        return self.submissions.count()


class HomeworkSubmission(models.Model):
    """
    Entrega de tarea realizada por un estudiante con soporte de archivo y retroalimentación docente.
    """
    class Status(models.TextChoices):
        SUBMITTED = 'SUBMITTED', 'Entregado a Tiempo'
        LATE = 'LATE', 'Entregado con Retardo'
        GRADED = 'GRADED', 'Calificado y Retroalimentado'

    homework = models.ForeignKey(
        Homework,
        on_delete=models.CASCADE,
        related_name='submissions',
        verbose_name='Tarea Asignada'
    )
    student = models.ForeignKey(
        'students.StudentProfile',
        on_delete=models.CASCADE,
        related_name='homework_submissions',
        verbose_name='Estudiante'
    )
    submission_text = models.TextField(blank=True, null=True, verbose_name='Comentario de Entrega')
    attachment = models.FileField(
        upload_to='homework_submissions/',
        blank=True,
        null=True,
        verbose_name='Archivo de Entrega (Trabajo del Estudiante)'
    )
    submitted_at = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de Envío')
    score = models.DecimalField(
        max_digits=4,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(Decimal('0.00')), MaxValueValidator(Decimal('10.00'))],
        verbose_name='Nota Obtenida (0.00 - 10.00)'
    )

    teacher_feedback = models.TextField(blank=True, null=True, verbose_name='Retroalimentación Docente')
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.SUBMITTED,
        verbose_name='Estado'
    )

    class Meta:
        verbose_name = 'Entrega de Tarea'
        verbose_name_plural = 'Entregas de Tareas'
        unique_together = ('homework', 'student')
        ordering = ['-submitted_at']

    def __str__(self):
        return f"{self.student.user.last_name} -> {self.homework.title}"

    @property
    def badge_class(self):
        mapping = {
            self.Status.SUBMITTED: 'bg-primary text-white',
            self.Status.LATE: 'bg-warning text-dark',
            self.Status.GRADED: 'bg-success text-white',
        }
        return mapping.get(self.status, 'bg-secondary text-white')
