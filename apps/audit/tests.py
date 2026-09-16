from django.test import TestCase, RequestFactory
from django.core.exceptions import PermissionDenied
from apps.accounts.models import CustomUser
from apps.accounts.services import create_institutional_user
from apps.audit.models import AuditLog
from apps.audit.services import log_audit

class AuditLogTests(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = create_institutional_user(
            username='auditor_test',
            email='auditor@academix.edu.co',
            password='Password123*',
            role=CustomUser.Role.ADMIN
        )

    def test_log_creation_and_values(self):
        request = self.factory.get('/dashboard/')
        request.user = self.user

        log = log_audit(
            action=AuditLog.Action.UPDATE,
            table_name='GradeRecord',
            record_id=101,
            old_values={'score': '3.50'},
            new_values={'score': '4.20'},
            reason='Corrección justificada de nota',
            user=self.user,
            request=request
        )

        self.assertIsNotNone(log.id)
        self.assertEqual(log.action, AuditLog.Action.UPDATE)
        self.assertEqual(log.table_name, 'GradeRecord')
        self.assertEqual(log.old_values.get('score'), '3.50')
        self.assertEqual(log.new_values.get('score'), '4.20')
        self.assertEqual(log.user, self.user)

    def test_immutability_on_update(self):
        log = log_audit(
            action=AuditLog.Action.INSERT,
            table_name='CustomUser',
            record_id=1,
            reason='Creación de usuario',
            user=self.user
        )
        # Intentar modificar el registro debe lanzar PermissionDenied
        log.reason = 'Modificación no autorizada'
        with self.assertRaises(PermissionDenied):
            log.save()

    def test_immutability_on_delete(self):
        log = log_audit(
            action=AuditLog.Action.INSERT,
            table_name='CustomUser',
            record_id=1,
            reason='Creación de usuario',
            user=self.user
        )
        # Intentar eliminar el registro debe lanzar PermissionDenied
        with self.assertRaises(PermissionDenied):
            log.delete()
