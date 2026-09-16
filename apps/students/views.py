from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import StudentProfile, Enrollment
from .services import enroll_student_in_section, get_or_create_student_profile
from apps.courses.models import CourseSection, AcademicYear
from apps.accounts.models import CustomUser
from apps.courses.services import get_current_academic_year

@login_required
def students_list_view(request):
    """
    Directorio de expedientes estudiantiles y estado de matrículas.
    """
    current_year = get_current_academic_year()
    section_id = request.GET.get('section')
    query = request.GET.get('q', '').strip()

    sections = CourseSection.objects.filter(academic_year=current_year).select_related('grade_level') if current_year else []
    enrollments = Enrollment.objects.filter(academic_year=current_year).select_related('student__user', 'student__parent', 'course_section__grade_level') if current_year else []

    if section_id:
        enrollments = enrollments.filter(course_section_id=section_id)
    if query:
        enrollments = enrollments.filter(
            student__user__first_name__icontains=query
        ) | enrollments.filter(
            student__user__last_name__icontains=query
        ) | enrollments.filter(
            student__student_code__icontains=query
        )

    # Estudiantes sin matricular en el año actual (para el modal de matrícula)
    enrolled_student_ids = Enrollment.objects.filter(academic_year=current_year).values_list('student__user_id', flat=True) if current_year else []
    available_users = CustomUser.objects.filter(role=CustomUser.Role.STUDENT, is_active=True).exclude(id__in=enrolled_student_ids)

    context = {
        'current_year': current_year,
        'sections': sections,
        'enrollments': enrollments,
        'available_users': available_users,
        'selected_section_id': section_id,
        'query': query,
    }
    return render(request, 'students/list.html', context)

@login_required
def enroll_student_view(request):
    """
    Registra formalmente una matrícula en un curso mediante modal o petición POST.
    """
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        section_id = request.POST.get('section_id')
        year_id = request.POST.get('academic_year_id')
        student_code = request.POST.get('student_code', '').strip()

        user = get_object_or_404(CustomUser, id=user_id, role=CustomUser.Role.STUDENT)
        section = get_object_or_404(CourseSection, id=section_id)
        academic_year = get_object_or_404(AcademicYear, id=year_id)

        try:
            profile = get_or_create_student_profile(user, student_code=student_code or None)
            enroll_student_in_section(
                student_profile=profile,
                course_section=section,
                academic_year=academic_year,
                user=request.user
            )
            messages.success(request, f'Estudiante {user.get_full_name()} matriculado exitosamente en {section.name}.')
        except Exception as e:
            messages.error(request, f'Error al matricular estudiante: {str(e)}')

    return redirect('students:list')


@login_required
def create_student_view(request):
    """
    Registra un nuevo alumno en la institución (Usuario, Perfil y Matrícula) en un solo paso.
    Exclusivo para Secretaría y Directivos.
    """
    if not (request.user.is_admin_role or request.user.is_rector or request.user.is_secretary):
        messages.error(request, 'No tiene permisos para registrar nuevos alumnos.')
        return redirect('students:list')

    if request.method == 'POST':
        from apps.accounts.services import create_institutional_user
        from apps.audit.services import log_audit

        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        doc_type = request.POST.get('document_type', 'TI')
        doc_num = request.POST.get('document_number', '').strip()
        student_code = request.POST.get('student_code', '').strip()
        email = request.POST.get('email', '').strip()
        phone = request.POST.get('phone', '').strip()
        section_id = request.POST.get('section_id')
        parent_id = request.POST.get('parent_id')

        # Si no se define código, auto-generar uno
        if not student_code:
            student_code = f"EST-{doc_num[-6:] if len(doc_num)>=6 else doc_num}"

        # Username único basado en documento o nombre
        username = f"est_{doc_num}" if doc_num else f"{first_name.lower()[:3]}{last_name.lower()[:3]}"
        if CustomUser.objects.filter(username=username).exists():
            username = f"{username}_{CustomUser.objects.count() + 1}"

        if not email:
            email = f"{username}@academix.edu.co"

        # Contraseña inicial = documento o 'estudiante123'
        password = doc_num if doc_num else 'estudiante123'

        try:
            with __import__('django').db.transaction.atomic():
                # 1. Crear CustomUser con rol STUDENT
                user = create_institutional_user(
                    username=username,
                    email=email,
                    password=password,
                    role=CustomUser.Role.STUDENT,
                    document_type=doc_type,
                    document_number=doc_num,
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone or None,
                    must_change_password=True
                )

                # 2. Crear StudentProfile
                parent_user = CustomUser.objects.filter(id=parent_id, role=CustomUser.Role.PARENT).first() if parent_id else None
                profile = get_or_create_student_profile(
                    user=user,
                    student_code=student_code,
                    parent=parent_user
                )

                # 3. Matricular en sección si se seleccionó
                current_year = get_current_academic_year()
                section_name = ""
                if section_id and current_year:
                    section = CourseSection.objects.get(id=section_id)
                    section_name = section.name
                    enroll_student_in_section(
                        student_profile=profile,
                        course_section=section,
                        academic_year=current_year,
                        user=request.user
                    )

                log_audit(
                    user=request.user,
                    action='CREATE_STUDENT',
                    table_name='StudentProfile',
                    record_id=profile.id,
                    new_values={'username': username, 'student_code': student_code, 'section': section_name},
                    reason=f'Registro de nuevo alumno por {request.user.username}',
                    request=request
                )

                messages.success(request, f'¡Estudiante {user.get_full_name()} registrado exitosamente! Usuario: {username} (Contraseña inicial: {password})')
        except Exception as e:
            messages.error(request, f'Error al registrar nuevo estudiante: {str(e)}')

    return redirect('students:list')

