from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import TeacherProfile, TeachingAssignment
from .services import assign_teacher_to_subject, get_or_create_teacher_profile
from apps.courses.models import CourseSection, AcademicYear
from apps.subjects.models import Subject
from apps.courses.services import get_current_academic_year

@login_required
def teachers_list_view(request):
    """
    Lista de docentes institucionales y gestión de carga académica.
    """
    current_year = get_current_academic_year()
    teachers = TeacherProfile.objects.select_related('user').all()
    assignments = TeachingAssignment.objects.filter(academic_year=current_year).select_related('teacher__user', 'course_section', 'subject') if current_year else []
    sections = CourseSection.objects.filter(academic_year=current_year) if current_year else []
    subjects = Subject.objects.all()

    context = {
        'current_year': current_year,
        'teachers': teachers,
        'assignments': assignments,
        'sections': sections,
        'subjects': subjects,
    }
    return render(request, 'teachers/list.html', context)

@login_required
def assign_teacher_view(request):
    """
    Crea o actualiza una asignación académica mediante formulario HTMX o POST tradicional.
    """
    if request.method == 'POST':
        teacher_id = request.POST.get('teacher_id')
        section_id = request.POST.get('section_id')
        subject_id = request.POST.get('subject_id')
        year_id = request.POST.get('academic_year_id')

        teacher = get_object_or_404(TeacherProfile, id=teacher_id)
        section = get_object_or_404(CourseSection, id=section_id)
        subject = get_object_or_404(Subject, id=subject_id)
        academic_year = get_object_or_404(AcademicYear, id=year_id)

        try:
            assign_teacher_to_subject(
                teacher=teacher,
                course_section=section,
                subject=subject,
                academic_year=academic_year,
                user=request.user
            )
            messages.success(request, f'Docente {teacher.user.get_full_name()} asignado a {subject.name} en {section.name}.')
        except Exception as e:
            messages.error(request, f'Error al asignar docente: {str(e)}')

    return redirect('teachers:list')


@login_required
def create_teacher_view(request):
    """
    Registra un nuevo docente en la planta institucional (Usuario y Perfil).
    Exclusivo para Directivos y Secretaría.
    """
    if not (request.user.is_admin_role or request.user.is_rector or request.user.is_secretary):
        messages.error(request, 'No tiene permisos para registrar nuevos docentes.')
        return redirect('teachers:list')

    if request.method == 'POST':
        from apps.accounts.models import CustomUser
        from apps.accounts.services import create_institutional_user
        from apps.audit.services import log_audit

        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        doc_type = request.POST.get('document_type', 'CC')
        doc_num = request.POST.get('document_number', '').strip()
        specialty = request.POST.get('specialty', '').strip() or 'Docente de Área'
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()

        username = f"doc_{doc_num}" if doc_num else f"{first_name.lower()[:3]}{last_name.lower()[:3]}"
        if CustomUser.objects.filter(username=username).exists():
            username = f"{username}_{CustomUser.objects.count() + 1}"

        if not email:
            email = f"{username}@academix.edu.co"

        password = doc_num if doc_num else 'docente123'

        try:
            with __import__('django').db.transaction.atomic():
                user = create_institutional_user(
                    username=username,
                    email=email,
                    password=password,
                    role=CustomUser.Role.TEACHER,
                    document_type=doc_type,
                    document_number=doc_num,
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone or None,
                    must_change_password=True
                )

                profile = get_or_create_teacher_profile(
                    user=user,
                    specialty=specialty
                )

                log_audit(
                    user=request.user,
                    action='CREATE_TEACHER',
                    table_name='TeacherProfile',
                    record_id=profile.id,
                    new_values={'username': username, 'specialty': specialty},
                    reason=f'Registro de nuevo docente por {request.user.username}',
                    request=request
                )

                messages.success(request, f'¡Docente {user.get_full_name()} registrado exitosamente! Usuario: {username} (Contraseña inicial: {password})')
        except Exception as e:
            messages.error(request, f'Error al registrar docente: {str(e)}')

    return redirect('teachers:list')

