from datetime import date
from decimal import Decimal
from django.core.management.base import BaseCommand
from apps.courses.models import AcademicYear, GradeLevel, CourseSection
from apps.courses.services import set_current_academic_year, create_course_section
from apps.periods.services import create_standard_periods
from apps.subjects.models import KnowledgeArea, Subject
from apps.subjects.services import configure_grade_subject
from apps.accounts.models import CustomUser
from apps.teachers.services import get_or_create_teacher_profile, assign_teacher_to_subject
from apps.students.services import get_or_create_student_profile, enroll_student_in_section

class Command(BaseCommand):
    help = 'Puebla la estructura académica inicial del Sistema ACADEMIX (Sprint 2)'

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Inicializando Estructura Académica (Sprint 2)...'))

        # 1. Año Lectivo 2026
        year2026, created = AcademicYear.objects.get_or_create(
            year=2026,
            defaults={
                'name': 'Año Escolar 2026',
                'start_date': date(2026, 1, 15),
                'end_date': date(2026, 11, 28),
                'status': AcademicYear.Status.ACTIVE,
                'is_current': True
            }
        )
        set_current_academic_year(year2026.id)
        self.stdout.write(self.style.SUCCESS(f' - Año Lectivo vigente confirmado: {year2026.name}'))

        # 2. Periodos Lectivos (1 al 4)
        periods = create_standard_periods(year2026)
        self.stdout.write(self.style.SUCCESS(f' - {len(periods)} Periodos Académicos configurados (25% c/u).'))

        # 3. Grados Escolares (Sexto a Once)
        grade_data = [
            ('Sexto', '06', GradeLevel.LevelStage.SECUNDARIA, 6),
            ('Séptimo', '07', GradeLevel.LevelStage.SECUNDARIA, 7),
            ('Octavo', '08', GradeLevel.LevelStage.SECUNDARIA, 8),
            ('Noveno', '09', GradeLevel.LevelStage.SECUNDARIA, 9),
            ('Décimo', '10', GradeLevel.LevelStage.MEDIA, 10),
            ('Once', '11', GradeLevel.LevelStage.MEDIA, 11),
        ]
        created_grades = {}
        for name, code, stage, order in grade_data:
            grade, _ = GradeLevel.objects.get_or_create(code=code, defaults={'name': name, 'level_stage': stage, 'order': order})
            created_grades[code] = grade
        self.stdout.write(self.style.SUCCESS(f' - {len(created_grades)} Grados Escolares confirmados.'))

        # 4. Áreas y Asignaturas
        areas_data = [
            ('Matemáticas', 1, [('Matemáticas Fundamentales', 'MAT-01'), ('Geometría y Estadística', 'GEO-01')]),
            ('Ciencias Naturales y Educación Ambiental', 2, [('Biología General', 'BIO-01'), ('Física Elemental', 'FIS-01')]),
            ('Humanidades y Lengua Castellana', 3, [('Lengua Castellana', 'ESP-01')]),
            ('Idioma Extranjero', 4, [('Inglés Comunicativo', 'ING-01')]),
            ('Tecnología e Informática', 5, [('Tecnología e Informática', 'TEC-01')]),
            ('Ciencias Sociales', 6, [('Historia y Geografía', 'SOC-01')]),
        ]

        all_subjects = []
        for area_name, a_order, subjects_list in areas_data:
            area, _ = KnowledgeArea.objects.get_or_create(name=area_name, defaults={'order': a_order})
            for s_name, s_code in subjects_list:
                subj, _ = Subject.objects.get_or_create(code=s_code, defaults={'name': s_name, 'area': area})
                all_subjects.append(subj)
                # Configurar intensidad en grado 6
                configure_grade_subject(created_grades['06'], subj, weekly_hours=4, weight_percentage=Decimal('100.00'))

        self.stdout.write(self.style.SUCCESS(f' - Áreas del conocimiento y {len(all_subjects)} Asignaturas registradas.'))

        # 5. Docente y Director de Grupo
        teacher_user = CustomUser.objects.filter(username='docente').first()
        teacher_profile = None
        if teacher_user:
            teacher_profile = get_or_create_teacher_profile(teacher_user, specialty='Licenciatura en Ciencias y Matemáticas')

        # 6. Secciones / Grupos para Grado 6°
        section_6a, _ = CourseSection.objects.get_or_create(
            academic_year=year2026,
            grade_level=created_grades['06'],
            name='6-A',
            defaults={'classroom': 'Aula 101', 'homeroom_teacher': teacher_user, 'capacity': 35}
        )
        section_6b, _ = CourseSection.objects.get_or_create(
            academic_year=year2026,
            grade_level=created_grades['06'],
            name='6-B',
            defaults={'classroom': 'Aula 102', 'capacity': 35}
        )
        self.stdout.write(self.style.SUCCESS(' - Cursos 6-A y 6-B creados.'))

        # 7. Asignación Académica Docente
        math_subject = Subject.objects.filter(code='MAT-01').first()
        if teacher_profile and math_subject:
            assign_teacher_to_subject(teacher_profile, section_6a, math_subject, year2026)
            assign_teacher_to_subject(teacher_profile, section_6b, math_subject, year2026)
            self.stdout.write(self.style.SUCCESS(f' - Asignación académica vinculada: Docente Diego -> {math_subject.name} (6-A y 6-B)'))

        # 8. Expediente y Matrícula de Estudiante
        student_user = CustomUser.objects.filter(username='estudiante').first()
        parent_user = CustomUser.objects.filter(username='acudiente').first()
        if student_user:
            student_profile = get_or_create_student_profile(student_user, student_code='EST-2026-0001', parent=parent_user)
            enroll_student_in_section(student_profile, section_6a, year2026)
            self.stdout.write(self.style.SUCCESS(' - Estudiante Esteban matriculado en curso 6-A.'))

        self.stdout.write(self.style.SUCCESS('¡Estructura académica de Sprint 2 inicializada con éxito!'))
