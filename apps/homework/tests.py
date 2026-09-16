from datetime import timedelta
from decimal import Decimal
from django.test import TestCase
from django.utils import timezone
from apps.accounts.models import CustomUser
from apps.accounts.services import create_institutional_user
from apps.courses.models import AcademicYear, GradeLevel, CourseSection
from apps.subjects.models import KnowledgeArea, Subject
from apps.periods.models import AcademicPeriod
from apps.teachers.models import TeacherProfile
from apps.teachers.services import get_or_create_teacher_profile
from apps.students.models import StudentProfile
from apps.students.services import get_or_create_student_profile, enroll_student_in_section
from .models import Homework, HomeworkSubmission
from .services import create_homework, submit_homework, grade_submission

class HomeworkTests(TestCase):
    def setUp(self):
        self.year = AcademicYear.objects.create(
            year=2026,
            name='Año 2026',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=300),
            status=AcademicYear.Status.ACTIVE,
            is_current=True
        )
        self.period = AcademicPeriod.objects.create(
            academic_year=self.year,
            number=1,
            name='Periodo 1',
            start_date=timezone.now().date(),
            end_date=timezone.now().date() + timedelta(days=90),
            percentage=Decimal('25.00'),
            status=AcademicPeriod.Status.ACTIVE
        )
        self.grade = GradeLevel.objects.create(name='Sexto', code='06', order=6)
        self.section = CourseSection.objects.create(academic_year=self.year, grade_level=self.grade, name='6-A')
        self.area = KnowledgeArea.objects.create(name='Ciencias', order=2)
        self.subject = Subject.objects.create(area=self.area, name='Biología', code='BIO-01')

        self.teacher_user = create_institutional_user(
            username='docente_bio',
            email='bio@academix.edu.co',
            password='Password123*',
            role=CustomUser.Role.TEACHER
        )
        self.teacher = get_or_create_teacher_profile(self.teacher_user, specialty='Licenciada en Biología')

        self.student_user = create_institutional_user(
            username='estudiante_hw',
            email='hw@academix.edu.co',
            password='Password123*',
            role=CustomUser.Role.STUDENT
        )
        self.student = get_or_create_student_profile(self.student_user, student_code='EST-HW-01')
        enroll_student_in_section(self.student, self.section, self.year)

    def test_homework_lifecycle(self):
        # 1. Crear tarea
        due = timezone.now() + timedelta(days=5)
        hw = create_homework(
            teacher=self.teacher,
            course_section=self.section,
            subject=self.subject,
            academic_period=self.period,
            title='Taller sobre Células Procariotas',
            description='Responder el cuestionario de las páginas 45 a 48.',
            due_date=due
        )
        self.assertEqual(hw.title, 'Taller sobre Células Procariotas')
        self.assertFalse(hw.is_expired)

        # 2. Entregar tarea
        submission = submit_homework(
            homework=hw,
            student=self.student,
            submission_text='Envío la solución a los 5 puntos del taller.'
        )
        self.assertEqual(submission.status, HomeworkSubmission.Status.SUBMITTED)

        # 3. Calificar entrega
        graded = grade_submission(submission.id, '4.80', feedback='Excelente desarrollo conceptual.')
        self.assertEqual(graded.score, Decimal('4.80'))
        self.assertEqual(graded.status, HomeworkSubmission.Status.GRADED)
