from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import PermissionDenied, ValidationError
from apps.accounts.models import CustomUser
from apps.courses.models import AcademicYear, GradeLevel, CourseSection
from apps.subjects.models import KnowledgeArea, Subject
from apps.periods.models import AcademicPeriod
from apps.teachers.models import TeacherProfile, TeachingAssignment
from apps.students.models import StudentProfile, Enrollment
from apps.grades.models import EvaluationCriterion, GradeRecord, PeriodFinalGrade
from apps.attendance.models import AttendanceSession, AttendanceRecord
from apps.rules.models import PromotionRule, AnnualFinalGrade, AcademicClosingLog
from apps.rules.services import (
    get_or_create_promotion_rule,
    close_academic_period,
    reopen_academic_period,
    calculate_annual_final_grades_for_student,
    evaluate_student_promotion,
    execute_annual_closing
)

class PromotionAndClosingRulesTestCase(TestCase):
    def setUp(self):
        self.admin = CustomUser.objects.create_superuser('admin_rules', 'admin@test.com', 'Pass123*')
        self.rector = CustomUser.objects.create_user('rector_rules', 'rector@test.com', 'Pass123*', role=CustomUser.Role.RECTOR)
        self.docente_user = CustomUser.objects.create_user('doc_rules', 'doc@test.com', 'Pass123*', role=CustomUser.Role.TEACHER)
        self.docente = TeacherProfile.objects.create(user=self.docente_user, specialty='Ciencias')

        self.student_user = CustomUser.objects.create_user('est_rules', 'est@test.com', 'Pass123*', role=CustomUser.Role.STUDENT)
        self.student = StudentProfile.objects.create(user=self.student_user, student_code='EST-TEST-01')

        self.year = AcademicYear.objects.create(
            year=2026,
            name='Año 2026 Test',
            start_date='2026-02-01',
            end_date='2026-11-30',
            status=AcademicYear.Status.ACTIVE,
            is_current=True
        )

        self.grade = GradeLevel.objects.create(name='Grado Sexto', code='6')
        self.section = CourseSection.objects.create(academic_year=self.year, grade_level=self.grade, name='6-A')

        self.enrollment = Enrollment.objects.create(
            student=self.student,
            course_section=self.section,
            academic_year=self.year,
            status=Enrollment.Status.ACTIVE
        )

        self.period1 = AcademicPeriod.objects.create(
            academic_year=self.year,
            number=1,
            name='Periodo 1',
            start_date='2026-02-01',
            end_date='2026-04-30',
            percentage=Decimal('25.00'),
            status=AcademicPeriod.Status.ACTIVE
        )
        self.period2 = AcademicPeriod.objects.create(
            academic_year=self.year,
            number=2,
            name='Periodo 2',
            start_date='2026-05-01',
            end_date='2026-07-31',
            percentage=Decimal('25.00'),
            status=AcademicPeriod.Status.ACTIVE
        )

        self.area = KnowledgeArea.objects.create(name='Matemáticas y Ciencias')
        self.sub_mat = Subject.objects.create(name='Matemáticas', code='MAT', area=self.area)
        self.sub_esp = Subject.objects.create(name='Español', code='ESP', area=self.area)
        self.sub_cie = Subject.objects.create(name='Ciencias', code='CIE', area=self.area)
        self.sub_ing = Subject.objects.create(name='Inglés', code='ING', area=self.area)

    def test_close_and_reopen_academic_period(self):
        """Prueba cierre y reapertura auditada de periodos lectivos."""
        # Docente no puede cerrar periodo
        with self.assertRaises(PermissionDenied):
            close_academic_period(self.period1, self.docente_user)

        # Rector cierra periodo
        closed_period = close_academic_period(self.period1, self.rector, 'Fin regular de periodo')
        self.assertEqual(closed_period.status, AcademicPeriod.Status.CLOSED)
        self.assertFalse(closed_period.is_editable)

        # Reapertura requiere justificación >= 10 chars
        with self.assertRaises(ValidationError):
            reopen_academic_period(self.period1, self.rector, 'corta')

        reopened = reopen_academic_period(self.period1, self.rector, 'Reapertura formal autorizada por consejo directivo')
        self.assertEqual(reopened.status, AcademicPeriod.Status.ACTIVE)
        self.assertTrue(reopened.is_editable)

    def test_promotion_rule_student_promoted(self):
        """Prueba estudiante promovido al aprobar asignaturas."""
        # Crear notas definitivas aprobatorias en Periodo 1 y 2
        PeriodFinalGrade.objects.create(
            student=self.student,
            course_section=self.section,
            subject=self.sub_mat,
            academic_period=self.period1,
            final_score=Decimal('4.50'),
            is_approved=True
        )
        PeriodFinalGrade.objects.create(
            student=self.student,
            course_section=self.section,
            subject=self.sub_mat,
            academic_period=self.period2,
            final_score=Decimal('4.00'),
            is_approved=True
        )

        eval_result = evaluate_student_promotion(self.student, self.section, self.year)
        self.assertTrue(eval_result['is_promoted'])
        self.assertEqual(eval_result['status'], Enrollment.Status.PROMOTED)
        self.assertEqual(eval_result['failed_count'], 0)

    def test_promotion_rule_student_failed_by_subjects(self):
        """Prueba reprobación si pierde 3 asignaturas anuales."""
        # Reprobar MAT, ESP y CIE
        for sub in [self.sub_mat, self.sub_esp, self.sub_cie]:
            PeriodFinalGrade.objects.create(
                student=self.student,
                course_section=self.section,
                subject=sub,
                academic_period=self.period1,
                final_score=Decimal('2.00'),
                is_approved=False
            )

        eval_result = evaluate_student_promotion(self.student, self.section, self.year)
        self.assertFalse(eval_result['is_promoted'])
        self.assertEqual(eval_result['status'], Enrollment.Status.FAILED)
        self.assertEqual(eval_result['failed_count'], 3)
        self.assertIn("Reprobó 3 asignaturas", eval_result['reason'])

    def test_promotion_rule_student_failed_by_absences(self):
        """Prueba reprobación si ausentismo acumulado >= 20%."""
        # Asignatura aprobada
        PeriodFinalGrade.objects.create(
            student=self.student,
            course_section=self.section,
            subject=self.sub_mat,
            academic_period=self.period1,
            final_score=Decimal('4.80'),
            is_approved=True
        )

        # Crear 10 sesiones de asistencia con 3 faltas injustificadas (30% ausentismo)
        for i in range(1, 11):
            sess = AttendanceSession.objects.create(
                course_section=self.section,
                subject=self.sub_mat,
                academic_period=self.period1,
                date=f'2026-02-{i:02d}',
                recorded_by=self.docente_user
            )
            status = AttendanceRecord.Status.UNJUSTIFIED if i <= 3 else AttendanceRecord.Status.PRESENT
            AttendanceRecord.objects.create(session=sess, student=self.student, status=status)

        eval_result = evaluate_student_promotion(self.student, self.section, self.year)
        self.assertFalse(eval_result['is_promoted'])
        self.assertEqual(eval_result['status'], Enrollment.Status.FAILED)
        self.assertIn("ausentismo", eval_result['reason'].lower())

    def test_execute_annual_closing(self):
        """Prueba ejecución atómica del cierre anual de año lectivo."""
        # Materia aprobada
        PeriodFinalGrade.objects.create(
            student=self.student,
            course_section=self.section,
            subject=self.sub_mat,
            academic_period=self.period1,
            final_score=Decimal('4.20'),
            is_approved=True
        )

        result = execute_annual_closing(self.year, self.rector, 'Cierre de fin de curso 2026')
        self.assertEqual(result['total_evaluated'], 1)
        self.assertEqual(result['total_promoted'], 1)
        self.assertEqual(result['total_failed'], 0)

        # Verificar matrícula actualizada a PROMOTED
        self.enrollment.refresh_from_db()
        self.assertEqual(self.enrollment.status, Enrollment.Status.PROMOTED)

        # Verificar año lectivo cerrado y periodos bloqueados
        self.year.refresh_from_db()
        self.assertEqual(self.year.status, AcademicYear.Status.CLOSED)
        self.assertFalse(self.year.is_current)

        self.period1.refresh_from_db()
        self.assertEqual(self.period1.status, AcademicPeriod.Status.LOCKED)
