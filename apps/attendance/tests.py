from datetime import date
from decimal import Decimal
from django.test import TestCase
from django.core.exceptions import PermissionDenied, ValidationError
from apps.accounts.models import CustomUser
from apps.accounts.services import create_institutional_user
from apps.courses.models import AcademicYear, GradeLevel, CourseSection
from apps.subjects.models import KnowledgeArea, Subject
from apps.periods.models import AcademicPeriod
from apps.students.models import StudentProfile, Enrollment
from apps.students.services import get_or_create_student_profile, enroll_student_in_section
from .models import AttendanceSession, AttendanceRecord
from .services import (
    get_or_create_attendance_session,
    update_student_attendance,
    calculate_student_absence_stats,
    mark_all_session_present
)

class AttendanceTests(TestCase):
    def setUp(self):
        self.year = AcademicYear.objects.create(
            year=2026,
            name='Año 2026',
            start_date=date(2026, 1, 15),
            end_date=date(2026, 11, 30),
            status=AcademicYear.Status.ACTIVE,
            is_current=True
        )
        self.period = AcademicPeriod.objects.create(
            academic_year=self.year,
            number=1,
            name='Periodo 1',
            start_date=date(2026, 1, 15),
            end_date=date(2026, 4, 1),
            percentage=Decimal('25.00'),
            status=AcademicPeriod.Status.ACTIVE
        )
        self.grade = GradeLevel.objects.create(name='Sexto', code='06', order=6)
        self.section = CourseSection.objects.create(academic_year=self.year, grade_level=self.grade, name='6-A')
        self.area = KnowledgeArea.objects.create(name='Matemáticas', order=1)
        self.subject = Subject.objects.create(area=self.area, name='Matemáticas Fundamentales', code='MAT-01')

        # Estudiante
        self.student_user = create_institutional_user(
            username='estudiante_test',
            email='test@academix.edu.co',
            password='Password123*',
            role=CustomUser.Role.STUDENT
        )
        self.student_profile = get_or_create_student_profile(self.student_user, student_code='EST-TEST-01')
        enroll_student_in_section(self.student_profile, self.section, self.year)

    def test_create_session_populates_enrolled_students(self):
        session = get_or_create_attendance_session(
            course_section=self.section,
            subject=self.subject,
            session_date=date(2026, 2, 10)
        )
        self.assertEqual(session.records.count(), 1)
        record = session.records.first()
        self.assertEqual(record.student, self.student_profile)
        self.assertEqual(record.status, AttendanceRecord.Status.UNJUSTIFIED)

    def test_update_attendance_and_absence_calculation(self):
        session1 = get_or_create_attendance_session(self.section, self.subject, date(2026, 2, 10))
        session2 = get_or_create_attendance_session(self.section, self.subject, date(2026, 2, 11))

        # Falta injustificada en sesión 1
        update_student_attendance(session1, self.student_profile, AttendanceRecord.Status.UNJUSTIFIED)
        
        # Presente en sesión 2
        update_student_attendance(session2, self.student_profile, AttendanceRecord.Status.PRESENT)

        stats = calculate_student_absence_stats(self.student_profile, self.subject, self.period)
        self.assertEqual(stats['total_sessions'], 2)
        self.assertEqual(stats['unjustified_hours'], 1)
        # 1 falta de 2 horas = 50.00%
        self.assertEqual(stats['absence_percentage'], Decimal('50.00'))
        self.assertEqual(stats['semaphore'], 'RED')
        self.assertTrue(stats['is_blocked'])

    def test_closed_period_prevents_modifications(self):
        self.period.status = AcademicPeriod.Status.CLOSED
        self.period.save()

        with self.assertRaises((PermissionDenied, ValidationError)):
            get_or_create_attendance_session(self.section, self.subject, date(2026, 2, 12))

    def test_mark_all_present(self):
        session = get_or_create_attendance_session(self.section, self.subject, date(2026, 2, 10))
        update_student_attendance(session, self.student_profile, AttendanceRecord.Status.UNJUSTIFIED)
        self.assertEqual(session.records.first().status, AttendanceRecord.Status.UNJUSTIFIED)

        mark_all_session_present(session)
        self.assertEqual(session.records.first().status, AttendanceRecord.Status.PRESENT)
