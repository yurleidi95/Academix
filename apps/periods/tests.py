from decimal import Decimal
from datetime import date
from django.test import TestCase
from .models import AcademicPeriod
from apps.courses.models import AcademicYear
from .services import change_period_status, create_standard_periods

class PeriodsTests(TestCase):
    def setUp(self):
        self.year = AcademicYear.objects.create(
            year=2026,
            name='Año 2026',
            start_date=date(2026, 1, 15),
            end_date=date(2026, 11, 30),
            status=AcademicYear.Status.ACTIVE,
            is_current=True
        )

    def test_create_standard_periods(self):
        periods = create_standard_periods(self.year)
        self.assertEqual(len(periods), 4)
        total_percentage = sum(p.percentage for p in periods)
        self.assertEqual(total_percentage, Decimal('100.00'))

    def test_change_status_audit(self):
        period = AcademicPeriod.objects.create(
            academic_year=self.year,
            number=1,
            name='Periodo 1',
            start_date=date(2026, 1, 15),
            end_date=date(2026, 4, 1),
            percentage=Decimal('25.00'),
            status=AcademicPeriod.Status.ACTIVE
        )
        updated = change_period_status(period.id, AcademicPeriod.Status.CLOSED, reason='Cierre reglamentario')
        self.assertEqual(updated.status, AcademicPeriod.Status.CLOSED)
        self.assertFalse(updated.is_editable)
