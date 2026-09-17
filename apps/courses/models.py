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


class InstitutionSetting(models.Model):
    """
    Configuración adaptable de la institución educativa.
    Permite que ACADEMIX funcione para Colegios, Universidades, Institutos Técnicos (SENA) o Academias.
    """
    class InstitutionType(models.TextChoices):
        COLEGIO = 'COLEGIO', 'Colegio / Escuela (Básica y Media)'
        UNIVERSIDAD = 'UNIVERSIDAD', 'Universidad / Educación Superior'
        SENA_TECNICO = 'SENA_TECNICO', 'Instituto Técnico / Tecnológico / SENA'
        ACADEMIA = 'ACADEMIA', 'Academia / Educación Continua'
        OTRO = 'OTRO', 'Institución Personalizada'

    institution_type = models.CharField(
        max_length=20,
        choices=InstitutionType.choices,
        default=InstitutionType.COLEGIO,
        verbose_name='Tipo de Institución'
    )
    institution_name = models.CharField(
        max_length=150,
        default='ACADEMIX',
        verbose_name='Nombre de la Institución'
    )
    slogan = models.CharField(
        max_length=255,
        blank=True,
        default='Sistema Integral de Gestión Académica y Control Escolar',
        verbose_name='Lema o Subtítulo'
    )

    # Terminología Adaptable
    term_student = models.CharField(max_length=30, default='Estudiante', verbose_name='Término Alumno (Singular)')
    term_students = models.CharField(max_length=30, default='Estudiantes', verbose_name='Término Alumnos (Plural)')
    term_teacher = models.CharField(max_length=30, default='Docente', verbose_name='Término Profesor (Singular)')
    term_teachers = models.CharField(max_length=30, default='Docentes', verbose_name='Término Profesores (Plural)')
    term_grade = models.CharField(max_length=30, default='Grado', verbose_name='Término Nivel/Grado (ej. Semestre/Grado/Ciclo)')
    term_section = models.CharField(max_length=30, default='Curso', verbose_name='Término Grupo/Curso (ej. Ficha/Curso/Grupo)')
    term_sections = models.CharField(max_length=30, default='Cursos', verbose_name='Término Grupos/Cursos (Plural)')
    term_subject = models.CharField(max_length=30, default='Asignatura', verbose_name='Término Materia (ej. Módulo/Competencia)')
    term_subjects = models.CharField(max_length=30, default='Asignaturas', verbose_name='Término Materias (Plural)')
    term_director = models.CharField(max_length=30, default='Rector(a)', verbose_name='Término Director(a)/Decano(a)')

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Configuración Institucional'
        verbose_name_plural = 'Configuración Institucional'

    def __str__(self):
        return f"{self.institution_name} ({self.get_institution_type_display()})"

    @classmethod
    def get_settings(cls):
        """Retorna la configuración activa o crea una por defecto."""
        setting, _ = cls.objects.get_or_create(id=1)
        return setting

    def apply_preset(self, preset_type):
        """Aplica terminología estándar según el tipo de entidad educativa."""
        self.institution_type = preset_type
        if preset_type == self.InstitutionType.UNIVERSIDAD:
            self.term_student = 'Estudiante'
            self.term_students = 'Estudiantes'
            self.term_teacher = 'Profesor(a)'
            self.term_teachers = 'Profesores'
            self.term_grade = 'Semestre'
            self.term_section = 'Grupo'
            self.term_sections = 'Grupos'
            self.term_subject = 'Materia'
            self.term_subjects = 'Materias'
            self.term_director = 'Decano(a) / Rector(a)'
        elif preset_type == self.InstitutionType.SENA_TECNICO:
            self.term_student = 'Aprendiz'
            self.term_students = 'Aprendices'
            self.term_teacher = 'Instructor(a)'
            self.term_teachers = 'Instructores'
            self.term_grade = 'Nivel / Trimestre'
            self.term_section = 'Ficha'
            self.term_sections = 'Fichas'
            self.term_subject = 'Competencia / Módulo'
            self.term_subjects = 'Competencias'
            self.term_director = 'Subdirector(a) de Centro'
        elif preset_type == self.InstitutionType.ACADEMIA:
            self.term_student = 'Alumno(a)'
            self.term_students = 'Alumnos'
            self.term_teacher = 'Tutor(a)'
            self.term_teachers = 'Tutores'
            self.term_grade = 'Nivel'
            self.term_section = 'Grupo / Clase'
            self.term_sections = 'Grupos'
            self.term_subject = 'Módulo / Taller'
            self.term_subjects = 'Módulos'
            self.term_director = 'Director(a)'
        else: # COLEGIO
            self.term_student = 'Estudiante'
            self.term_students = 'Estudiantes'
            self.term_teacher = 'Docente'
            self.term_teachers = 'Docentes'
            self.term_grade = 'Grado'
            self.term_section = 'Curso'
            self.term_sections = 'Cursos'
            self.term_subject = 'Asignatura'
            self.term_subjects = 'Asignaturas'
            self.term_director = 'Rector(a)'
        self.save()

