from django.core.management.base import BaseCommand
from apps.accounts.services import setup_roles_and_permissions, create_institutional_user
from apps.accounts.models import CustomUser

class Command(BaseCommand):
    help = 'Inicializa los grupos de roles y crea usuarios institucionales base para pruebas'

    def add_arguments(self, parser):
        parser.add_argument(
            '--create-demos',
            action='store_true',
            help='Crea usuarios demostrativos para cada uno de los 6 roles'
        )

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE('Inicializando grupos y permisos de roles ACADEMIX...'))
        groups = setup_roles_and_permissions()
        for role, group in groups.items():
            self.stdout.write(self.style.SUCCESS(f' - Grupo confirmado: {group.name} [{role}]'))

        # Crear superadministrador por defecto si no existe
        if not CustomUser.objects.filter(username='admin').exists():
            admin_user = create_institutional_user(
                username='admin',
                email='admin@academix.edu.co',
                password='AdminPassword123*',
                role=CustomUser.Role.ADMIN,
                document_type=CustomUser.DocumentType.CC,
                document_number='1000000001',
                first_name='Administrador',
                last_name='Principal',
                phone='3001234567',
                address='Sede Principal ACADEMIX',
                is_staff=True,
                is_superuser=True
            )
            self.stdout.write(self.style.SUCCESS(f'Superusuario Administrador creado: admin (clave: AdminPassword123*)'))
        else:
            self.stdout.write(self.style.NOTICE('Usuario admin ya existe.'))

        if options.get('create_demos'):
            demos = [
                ('rector', 'rector@academix.edu.co', CustomUser.Role.RECTOR, '1000000002', 'Ramiro', 'Rectoría'),
                ('secretaria', 'secretaria@academix.edu.co', CustomUser.Role.SECRETARIA, '1000000003', 'Sonia', 'Secretaría'),
                ('docente', 'docente@academix.edu.co', CustomUser.Role.TEACHER, '1000000004', 'Diego', 'Docente'),
                ('estudiante', 'estudiante@academix.edu.co', CustomUser.Role.STUDENT, '1000000005', 'Esteban', 'Estudiante'),
                ('acudiente', 'acudiente@academix.edu.co', CustomUser.Role.PARENT, '1000000006', 'Patricia', 'Padre de Familia'),
            ]
            for uname, email, role, doc, fname, lname in demos:
                if not CustomUser.objects.filter(username=uname).exists():
                    create_institutional_user(
                        username=uname,
                        email=email,
                        password='DemoPassword123*',
                        role=role,
                        document_type=CustomUser.DocumentType.CC,
                        document_number=doc,
                        first_name=fname,
                        last_name=lname,
                        phone='3100000000',
                        address='Ciudad Escolar'
                    )
                    self.stdout.write(self.style.SUCCESS(f'Usuario demo {uname} ({role}) creado.'))

        self.stdout.write(self.style.SUCCESS('¡Inicialización de roles completada con éxito!'))
