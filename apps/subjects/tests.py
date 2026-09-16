from decimal import Decimal
from django.test import TestCase
from .models import KnowledgeArea, Subject, GradeSubject
from apps.courses.models import GradeLevel
from .services import configure_grade_subject

class SubjectsTests(TestCase):
    def setUp(self):
        self.area = KnowledgeArea.objects.create(name='Matemáticas', order=1)
        self.subject = Subject.objects.create(
            area=self.area,
            name='Álgebra',
            code='MAT-ALG'
        )
        self.grade = GradeLevel.objects.create(
            name='Octavo',
            code='08',
            level_stage=GradeLevel.LevelStage.SECUNDARIA,
            order=8
        )

    def test_grade_subject_configuration(self):
        gs = configure_grade_subject(
            grade_level=self.grade,
            subject=self.subject,
            weekly_hours=5,
            weight_percentage=Decimal('100.00')
        )
        self.assertEqual(gs.weekly_hours, 5)
        self.assertEqual(gs.weight_percentage, Decimal('100.00'))
        self.assertEqual(GradeSubject.objects.count(), 1)

    def test_decimal_precision(self):
        gs = configure_grade_subject(
            grade_level=self.grade,
            subject=self.subject,
            weekly_hours=4,
            weight_percentage=Decimal('60.50')
        )
        self.assertIsInstance(gs.weight_percentage, Decimal)
        self.assertEqual(gs.weight_percentage, Decimal('60.50'))
