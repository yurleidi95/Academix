from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.db import transaction
from django.contrib.auth import authenticate, login
from .models import CustomUser

# Nombres canónicos de grupos
ROLE_GROUPS = {
    CustomUser.Role.ADMIN: 'Administradores',
    CustomUser.Role.RECTOR: 'Directivos Rectores',
    CustomUser.Role.SECRETARIA: 'Secretaría Académica',
    CustomUser.Role.TEACHER: 'Docentes',
    CustomUser.Role.STUDENT: 'Estudiantes',
    CustomUser.Role.PARENT: 'Padres y Acudientes',
}

def setup_roles_and_permissions():
    """
    Crea o sincroniza los grupos de permisos estándar para los 6 roles de ACADEMIX.
    """
    created_groups = {}
    for role_code, group_name in ROLE_GROUPS.items():
        group, created = Group.objects.get_or_create(name=group_name)
        created_groups[role_code] = group
    return created_groups

@transaction.atomic
def create_institutional_user(
    username,
    email,
    password,
    role,
    document_type=CustomUser.DocumentType.CC,
    document_number=None,
    first_name='',
    last_name='',
    phone=None,
    address=None,
    must_change_password=False,
    is_staff=False,
    is_superuser=False
):
    """
    Crea un usuario institucional con su rol asignado, pertenencia a grupo y validaciones.
    """
    # Si es admin o rector, se puede conceder staff para acceso a Django Admin si se requiere
    if role in [CustomUser.Role.ADMIN, CustomUser.Role.RECTOR]:
        is_staff = True
    if role == CustomUser.Role.ADMIN and is_superuser:
        is_superuser = True

    user = CustomUser.objects.create_user(
        username=username,
        email=email,
        password=password,
        role=role,
        document_type=document_type,
        document_number=document_number,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        address=address,
        must_change_password=must_change_password,
        is_staff=is_staff,
        is_superuser=is_superuser,
    )

    # Asignar al grupo correspondiente al rol
    group_name = ROLE_GROUPS.get(role)
    if group_name:
        group, _ = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)

    return user

def assign_role_group(user):
    """
    Asegura que el usuario pertenezca al grupo asignado a su rol actual.
    """
    group_name = ROLE_GROUPS.get(user.role)
    if group_name:
        group, _ = Group.objects.get_or_create(name=group_name)
        # Limpiar grupos previos de roles y asignar el nuevo
        for r_code, r_group_name in ROLE_GROUPS.items():
            if r_group_name != group_name:
                try:
                    old_group = Group.objects.get(name=r_group_name)
                    user.groups.remove(old_group)
                except Group.DoesNotExist:
                    pass
        user.groups.add(group)
