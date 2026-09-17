"""
Comando de gestión: reset_users
Uso: python manage.py reset_users [--confirm] [--keep-superusers]

Limpia todos los usuarios registrados (excepto superusuarios si se indica),
sus perfiles de estudiante, docente y matrículas asociadas.
Útil para reiniciar el sistema en ambientes de prueba o para permitir
que todos se registren desde cero.
"""
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = (
        'Elimina todos los usuarios del sistema (excepto superusuarios) '
        'para permitir que cada persona se registre nuevamente desde cero.'
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--confirm',
            action='store_true',
            default=False,
            help='Confirmar la eliminación sin solicitud interactiva.',
        )
        parser.add_argument(
            '--keep-superusers',
            action='store_true',
            default=True,
            help='Mantener los superusuarios de Django (por defecto: sí).',
        )

    def handle(self, *args, **options):
        from apps.accounts.models import CustomUser
        from apps.students.models import StudentProfile, Enrollment, StudentObservation
        from apps.teachers.models import TeacherProfile

        confirm = options['confirm']
        keep_su = options['keep_superusers']

        if not confirm:
            self.stdout.write(
                self.style.WARNING(
                    '\nADVERTENCIA: Esta operacion eliminara TODOS los usuarios del sistema '
                    '(estudiantes, docentes, padres, secretarias, rectores).\n'
                    'Los datos de matriculas, observaciones y perfiles asociados tambien seran eliminados.\n'
                    'Esta accion NO se puede deshacer.\n'
                )
            )
            respuesta = input('Esta seguro que desea continuar? Escriba "CONFIRMAR" para proceder: ')
            if respuesta.strip().upper() != 'CONFIRMAR':
                self.stdout.write(self.style.SUCCESS('Operacion cancelada. No se realizaron cambios.'))
                return

        qs = CustomUser.objects.all()
        if keep_su:
            qs = qs.filter(is_superuser=False)

        total = qs.count()

        with transaction.atomic():
            # Eliminar en orden de dependencias (FK en cascada, pero forzamos el orden)
            student_ids = list(StudentProfile.objects.filter(user__in=qs).values_list('id', flat=True))
            StudentObservation.objects.filter(student_id__in=student_ids).delete()
            Enrollment.objects.filter(student_id__in=student_ids).delete()
            StudentProfile.objects.filter(id__in=student_ids).delete()
            TeacherProfile.objects.filter(user__in=qs).delete()
            deleted_count, _ = qs.delete()

        if keep_su:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\nSe eliminaron {total} usuario(s) del sistema (superusuarios conservados).\n'
                    f'   El sistema esta listo para nuevos registros.'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'\nSe eliminaron TODOS los {total} usuario(s), incluyendo superusuarios.\n'
                    f'   Recuerde crear un nuevo superusuario: python manage.py createsuperuser'
                )
            )
