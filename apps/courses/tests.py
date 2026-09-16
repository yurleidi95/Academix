from django.test import TestCase
from datetime import date
from .models import AcademicYear, GradeLevel, CourseSection
from .services import set_current_academic_year, create_course_section

class CoursesTests(TestCase):
    def setUp(self):
        self.year2025 = AcademicYear.objects.create(
            year=2025,
            name='Año Escolar 2025',
            start_date=date(2025, 1, 15),
            end_date=date(2025, 11, 30),
            status=AcademicYear.Status.CLOSED,
            is_current=False
        )
        self.year2026 = AcademicYear.objects.create(
            year=2026,
            name='Año Escolar 2026',
            start_date=date(2026, 1, 15),
            end_date=date(2026, 11, 30),
            status=AcademicYear.Status.PLANNING,
            is_current=False
        )
        self.grade6 = GradeLevel.objects.create(
            name='Sexto',
            code='06',
            level_stage=GradeLevel.LevelStage.SECUNDARIA,
            order=6
        )

    def test_set_current_academic_year_exclusivity(self):
        # Marcar 2025 como actual
        set_current_academic_year(self.year2025.id)
        self.year2025.refresh_from_db()
        self.assertTrue(self.year2025.is_current)

        # Ahora marcar 2026 como actual, 2025 debe perder el flag
        set_current_academic_year(self.year2026.id)
        self.year2025.refresh_from_db()
        self.year2026.refresh_from_db()

        self.assertFalse(self.year2025.is_current)
        self.assertTrue(self.year2026.is_current)
        self.assertEqual(self.year2026.status, AcademicYear.Status.ACTIVE)

    def test_create_section_service(self):
        section = create_course_section(
            academic_year=self.year2026,
            grade_level=self.grade6,
            name='6-A',
            classroom='Aula 101',
            capacity=35
        )
        self.assertEqual(section.name, '6-A')
        self.assertEqual(section.academic_year, self.year2026)
        self.assertEqual(section.grade_level, self.grade6)
