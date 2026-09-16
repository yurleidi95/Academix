from datetime import date
from django.test import TestCase
from apps.accounts.models import CustomUser
from apps.accounts.services import create_institutional_user
from apps.courses.models import AcademicYear, GradeLevel, CourseSection
from .models import StudentProfile, Enrollment
from .services import enroll_student_in_section, get_or_create_student_profile

class StudentsTests(TestCase):
    def setUp(self):
        self.user = create_institutional_user(
            username='estudiante_juan',
            email='juan@academix.edu.co',
            password='Password123*',
            role=CustomUser.Role.STUDENT
        )
        self.profile = get_or_create_student_profile(self.user, student_code='EST-2026-001')

        self.year = AcademicYear.objects.create(
            year=2026,
            name='Año 2026',
            start_date=date(2026, 1, 15),
            end_date=date(2026, 11, 30),
            status=AcademicYear.Status.ACTIVE,
            is_current=True
        )
        self.grade = GradeLevel.objects.create(name='Sexto', code='06', order=6)
        self.section1 = CourseSection.objects.create(academic_year=self.year, grade_level=self.grade, name='6-A')
        self.section2 = CourseSection.objects.create(academic_year=self.year, grade_level=self.grade, name='6-B')

    def test_enrollment_success(self):
        enrollment = enroll_student_in_section(
            student_profile=self.profile,
            course_section=self.section1,
            academic_year=self.year
        )
        self.assertEqual(enrollment.student, self.profile)
        self.assertEqual(enrollment.course_section, self.section1)
        self.assertEqual(enrollment.status, Enrollment.Status.ACTIVE)

    def test_single_enrollment_per_year_update(self):
        # Matricular en 6-A
        enroll_student_in_section(
            student_profile=self.profile,
            course_section=self.section1,
            academic_year=self.year
        )
        # Trasladar a 6-B en el mismo año escolar actualiza la matrícula sin duplicar
        updated = enroll_student_in_section(
            student_profile=self.profile,
            course_section=self.section2,
            academic_year=self.year
        )
        self.assertEqual(Enrollment.objects.filter(student=self.profile, academic_year=self.year).count(), 1)
        self.assertEqual(updated.course_section, self.section2)
