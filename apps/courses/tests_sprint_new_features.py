from decimal import Decimal
from django.test import TestCase, Client
from django.urls import reverse
from apps.accounts.models import CustomUser
from apps.courses.models import AcademicYear, GradeLevel, CourseSection, InstitutionSetting
from apps.subjects.models import Subject
from apps.periods.models import AcademicPeriod
from apps.teachers.models import TeacherProfile, TeachingAssignment
from apps.students.models import StudentProfile, Enrollment, StudentObservation
from apps.homework.models import Homework, HomeworkSubmission
from apps.homework.services import grade_or_create_submission
from django.utils import timezone
from datetime import timedelta

class SprintNewFeaturesTests(TestCase):
    def setUp(self):
        # 1. Crear Año Lectivo y Periodo
        self.year = AcademicYear.objects.create(
            year=2026,
            name='Año 2026',
            start_date='2026-01-15',
            end_date='2026-11-30',
            status=AcademicYear.Status.ACTIVE,
            is_current=True
        )
        self.period = AcademicPeriod.objects.create(
            academic_year=self.year,
            number=1,
            name='Periodo 1',
            percentage=Decimal('25.00'),
            start_date='2026-01-15',
            end_date='2026-04-10',
            status=AcademicPeriod.Status.ACTIVE
        )
        self.grade = GradeLevel.objects.create(name='Décimo', code='10', order=10)
        self.section = CourseSection.objects.create(
            academic_year=self.year,
            grade_level=self.grade,
            name='10-A'
        )
        from apps.subjects.models import KnowledgeArea
        self.area = KnowledgeArea.objects.create(name='Ciencias Exactas', order=1)
        self.subject = Subject.objects.create(area=self.area, name='Matemáticas', code='MAT-10')

        # 2. Usuarios con roles
        self.admin = CustomUser.objects.create_superuser('admin_user', 'admin@test.com', 'adminpass')
        self.rector = CustomUser.objects.create_user('rector_user', 'rector@test.com', 'rectorpass', role=CustomUser.Role.RECTOR)
        self.secretaria = CustomUser.objects.create_user('sec_user', 'sec@test.com', 'secpass', role=CustomUser.Role.SECRETARIA)
        self.teacher_user = CustomUser.objects.create_user('docente_user', 'doc@test.com', 'docpass', role=CustomUser.Role.TEACHER)
        self.teacher_prof = TeacherProfile.objects.create(user=self.teacher_user, specialty='Matemáticas')

        self.assignment = TeachingAssignment.objects.create(
            teacher=self.teacher_prof,
            course_section=self.section,
            subject=self.subject,
            academic_year=self.year
        )

        self.parent_user = CustomUser.objects.create_user('padre_user', 'padre@test.com', 'padrepass', role=CustomUser.Role.PARENT)
        self.student_user = CustomUser.objects.create_user('est_user', 'est@test.com', 'estpass', role=CustomUser.Role.STUDENT, document_number='1001')
        self.student_prof = StudentProfile.objects.create(user=self.student_user, student_code='EST-1001', parent=self.parent_user)

        self.enrollment = Enrollment.objects.create(
            student=self.student_prof,
            course_section=self.section,
            academic_year=self.year,
            status=Enrollment.Status.ACTIVE
        )

        self.client = Client()

    def test_institution_adaptability_and_presets(self):
        """Valida que el modelo de configuración institucional aplique presets correctamente."""
        setting = InstitutionSetting.get_settings()
        self.assertEqual(setting.term_student, 'Estudiante')

        # Aplicar preset SENA Técnico
        setting.apply_preset(InstitutionSetting.InstitutionType.SENA_TECNICO)
        setting.refresh_from_db()
        self.assertEqual(setting.term_student, 'Aprendiz')
        self.assertEqual(setting.term_teacher, 'Instructor(a)')
        self.assertEqual(setting.term_section, 'Ficha')

        # Aplicar preset Universidad
        setting.apply_preset(InstitutionSetting.InstitutionType.UNIVERSIDAD)
        setting.refresh_from_db()
        self.assertEqual(setting.term_teacher, 'Profesor(a)')
        self.assertEqual(setting.term_section, 'Grupo')

    def test_student_observations_permissions(self):
        """Valida que Rector, Secretaria y Docente puedan poner observaciones y que Padre/Estudiante no puedan."""
        # 1. Docente crea observación
        self.client.login(username='docente_user', password='docpass')
        resp = self.client.post(reverse('students:create_observation', args=[self.student_prof.id]), {
            'title': 'Felicitación por rendimiento',
            'description': 'Excelente desempeño en la primera unidad de cálculo.',
            'category': StudentObservation.Category.RECOGNITION,
            'severity': StudentObservation.Severity.INFO,
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(StudentObservation.objects.filter(student=self.student_prof).count(), 1)
        self.client.logout()

        # 2. Rector crea observación
        self.client.login(username='rector_user', password='rectorpass')
        resp = self.client.post(reverse('students:create_observation', args=[self.student_prof.id]), {
            'title': 'Compromiso académico',
            'description': 'Revisión en rectoría de plan de estudios.',
            'category': StudentObservation.Category.ACADEMIC,
            'severity': StudentObservation.Severity.INFO,
        })
        self.assertEqual(resp.status_code, 302)
        self.assertEqual(StudentObservation.objects.filter(student=self.student_prof).count(), 2)
        self.client.logout()

        # 3. Padre intenta crear observación -> BLOQUEADO (403)
        self.client.login(username='padre_user', password='padrepass')
        resp = self.client.post(reverse('students:create_observation', args=[self.student_prof.id]), {
            'title': 'Intento no autorizado',
            'description': 'Texto',
        })
        self.assertEqual(resp.status_code, 403)

        # 4. Padre puede consultar el observador de su hijo en solo lectura (200)
        resp_view = self.client.get(reverse('students:observations', args=[self.student_prof.id]))
        self.assertEqual(resp_view.status_code, 200)
        self.assertContains(resp_view, 'Felicitación por rendimiento')
        self.client.logout()

    def test_parent_read_only_grades_and_attendance(self):
        """Valida que el padre de familia solo pueda consultar y tenga bloqueada la edición."""
        self.client.login(username='padre_user', password='padrepass')

        # 1. Consulta de notas en solo lectura
        resp_grades = self.client.get(reverse('grades:index'))
        self.assertEqual(resp_grades.status_code, 200)

        # 2. Intento de acceder a la planilla global -> Redirigido con error
        resp_matrix = self.client.get(reverse('grades:matrix'), {'section_id': self.section.id, 'subject_id': self.subject.id, 'period_id': self.period.id})
        self.assertEqual(resp_matrix.status_code, 302)

        # 3. Intento de enviar nota inline -> 403 Prohibido
        resp_post = self.client.post(reverse('grades:update_inline'), {
            'student_id': self.student_prof.id,
            'section_id': self.section.id,
            'subject_id': self.subject.id,
            'period_id': self.period.id,
            'score': '4.50'
        })
        self.assertEqual(resp_post.status_code, 403)

        # 4. Consulta de asistencia en solo lectura
        resp_att = self.client.get(reverse('attendance:index'))
        self.assertEqual(resp_att.status_code, 200)

        # 5. Intento de abrir planilla de llamado de lista -> Redirigido
        resp_sheet = self.client.get(reverse('attendance:sheet'), {'section_id': self.section.id, 'subject_id': self.subject.id})
        self.assertEqual(resp_sheet.status_code, 302)
        self.client.logout()

    def test_homework_course_matrix_and_manual_grading(self):
        """Valida el flujo de cursos en tareas y la calificación manual directa."""
        # Crear tarea para el curso
        hw = Homework.objects.create(
            teacher=self.teacher_prof,
            course_section=self.section,
            subject=self.subject,
            academic_period=self.period,
            title='Taller 1 de Vectores',
            description='Resolver los ejercicios del 1 al 10',
            due_date=timezone.now() + timedelta(days=5)
        )

        # 1. Docente ingresa a tareas y ve los cursos
        self.client.login(username='docente_user', password='docpass')
        resp_index = self.client.get(reverse('homework:index'))
        self.assertEqual(resp_index.status_code, 200)
        self.assertContains(resp_index, '10-A')

        # 2. Docente entra a la matriz del curso 10-A
        resp_matrix = self.client.get(reverse('homework:course_matrix', args=[self.section.id]))
        self.assertEqual(resp_matrix.status_code, 200)
        self.assertContains(resp_matrix, 'Taller 1 de Vectores')
        self.assertContains(resp_matrix, self.student_user.last_name)

        # 3. Docente califica manualmente al alumno
        resp_grade = self.client.post(reverse('homework:grade_cell'), {
            'homework_id': hw.id,
            'student_id': self.student_prof.id,
            'section_id': self.section.id,
            'score': '4.80',
            'feedback': 'Excelente trabajo presentado en clase'
        })
        self.assertEqual(resp_grade.status_code, 302)

        # Verificar que quedó registrado como GRADED con su nota
        sub = HomeworkSubmission.objects.get(homework=hw, student=self.student_prof)
        self.assertEqual(sub.score, Decimal('4.80'))
        self.assertEqual(sub.status, HomeworkSubmission.Status.GRADED)
        self.assertEqual(sub.teacher_feedback, 'Excelente trabajo presentado en clase')
        self.client.logout()

        # 4. El padre consulta la tarea y ve la nota (Solo Lectura)
        self.client.login(username='padre_user', password='padrepass')
        resp_parent_hw = self.client.get(reverse('homework:index'))
        self.assertEqual(resp_parent_hw.status_code, 200)
        self.assertTrue('4,80' in resp_parent_hw.content.decode('utf-8') or '4.80' in resp_parent_hw.content.decode('utf-8'))
        self.assertContains(resp_parent_hw, 'Excelente trabajo presentado en clase')
        self.client.logout()

    def test_bulk_student_upload(self):
        """Valida la carga masiva de alumnos para un curso específico."""
        self.client.login(username='docente_user', password='docpass')

        # Datos en texto pegado (documento, tipo, nombre, apellido)
        pasted_text = (
            "987654321	TI	Pedro	González	pedro@test.com	3001112233	EST-987\n"
            "987654322	TI	Lucía	Méndez	lucia@test.com	3004445566	EST-988\n"
        )

        resp = self.client.post(reverse('students:bulk_upload'), {
            'section_id': self.section.id,
            'raw_data': pasted_text,
        })
        self.assertEqual(resp.status_code, 302)

        # Verificar que ambos estudiantes se crearon y están matriculados en 10-A
        self.assertTrue(CustomUser.objects.filter(document_number='987654321').exists())
        self.assertTrue(CustomUser.objects.filter(document_number='987654322').exists())
        self.assertEqual(Enrollment.objects.filter(course_section=self.section).count(), 3) # 1 inicial + 2 masivos
        self.client.logout()
