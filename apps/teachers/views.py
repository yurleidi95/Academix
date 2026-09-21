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
    Lista de docentes institucionales y gestión de carga académica para la institución activa.
    """
    from apps.courses.models import InstitutionSetting
    inst_type = InstitutionSetting.get_settings().institution_type

    current_year = get_current_academic_year()
    teachers = TeacherProfile.objects.select_related('user').all()
    assignments = TeachingAssignment.objects.filter(
        academic_year=current_year,
        course_section__grade_level__institution_type=inst_type
    ).select_related('teacher__user', 'course_section', 'subject') if current_year else []
    sections = CourseSection.objects.filter(
        academic_year=current_year,
        grade_level__institution_type=inst_type
    ) if current_year else []
    subjects = Subject.objects.filter(institution_type=inst_type)

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


@login_required
def teacher_courses_view(request):
    """
    Vista principal "Mis Cursos" para el docente: listado de grupos asignados
    con acceso directo a su espacio de trabajo institucional.
    """
    from apps.courses.models import InstitutionSetting
    inst_type = InstitutionSetting.get_settings().institution_type
    current_year = get_current_academic_year()

    user = request.user
    if user.is_teacher and hasattr(user, 'teacher_profile'):
        assignments = TeachingAssignment.objects.filter(
            teacher=user.teacher_profile,
            academic_year=current_year,
            is_active=True
        ).select_related('course_section__grade_level', 'subject')

        section_ids = assignments.values_list('course_section_id', flat=True).distinct()
        sections = CourseSection.objects.filter(id__in=section_ids).select_related('grade_level')
    else:
        # Administradores y directivos pueden explorar todos los cursos
        sections = CourseSection.objects.filter(
            academic_year=current_year,
            grade_level__institution_type=inst_type
        ).select_related('grade_level')
        assignments = TeachingAssignment.objects.filter(academic_year=current_year).select_related('subject')

    courses_data = []
    for s in sections:
        sec_assignments = assignments.filter(course_section=s)
        student_count = s.enrollments.filter(status='ACTIVE').count()
        courses_data.append({
            'section': s,
            'assignments': sec_assignments,
            'subjects_count': sec_assignments.values('subject').distinct().count(),
            'students_count': student_count,
        })

    context = {
        'courses_data': courses_data,
        'current_year': current_year,
    }
    return render(request, 'teachers/my_courses.html', context)


@login_required
def course_workspace_view(request, section_id):
    """
    Espacio de trabajo del curso seleccionado por el docente con tres opciones clave:
    1. Asistencia (Llamado de lista y modificación)
    2. Malla Curricular (Intensidades horarias y Normas/Estándares asociados)
    3. Asignaturas (Agrupadas en Principales, Humanísticas y Arte/Deporte con acceso a evaluación)
    """
    from apps.subjects.models import Subject, SubjectNorm, GradeSubject
    from apps.periods.services import get_current_active_period
    from apps.attendance.models import AttendanceSheet, AttendanceRecord
    import datetime

    section = get_object_or_404(CourseSection.objects.select_related('grade_level', 'academic_year'), id=section_id)
    current_year = section.academic_year
    active_period = get_current_active_period(current_year) if current_year else None
    user = request.user

    # Verificar asignaciones del docente en este curso
    if user.is_teacher and hasattr(user, 'teacher_profile'):
        my_assignments = TeachingAssignment.objects.filter(
            teacher=user.teacher_profile,
            course_section=section,
            is_active=True
        ).select_related('subject')
        assigned_subject_ids = list(my_assignments.values_list('subject_id', flat=True))
    else:
        my_assignments = TeachingAssignment.objects.filter(
            course_section=section,
            is_active=True
        ).select_related('subject', 'teacher__user')
        assigned_subject_ids = list(my_assignments.values_list('subject_id', flat=True))

    # 1. Asignaturas agrupadas en Principales, Humanísticas y Arte/Deporte
    subjects_in_course = Subject.objects.filter(
        id__in=assigned_subject_ids
    ).prefetch_related('norms') if assigned_subject_ids else Subject.objects.filter(
        curriculum_grades__grade_level=section.grade_level
    ).prefetch_related('norms')

    principales = [s for s in subjects_in_course if s.category == Subject.Category.PRINCIPAL]
    humanisticas = [s for s in subjects_in_course if s.category == Subject.Category.HUMANISTICA]
    arte_deporte = [s for s in subjects_in_course if s.category == Subject.Category.ARTE_DEPORTE]

    # 2. Malla Curricular del Grado
    curriculum = GradeSubject.objects.filter(
        grade_level=section.grade_level
    ).select_related('subject__area').prefetch_related('subject__norms')

    # 3. Control de Asistencia del Curso
    active_enrollments = section.enrollments.filter(status='ACTIVE').select_related('student__user').order_by('student__user__last_name')
    date_str = request.GET.get('date', datetime.date.today().isoformat())
    try:
        current_date = datetime.date.fromisoformat(date_str)
    except ValueError:
        current_date = datetime.date.today()

    first_subj = subjects_in_course.first()
    sheet = None
    records_by_student = {}
    if first_subj:
        sheet = AttendanceSheet.objects.filter(
            course_section=section,
            subject=first_subj,
            date=current_date
        ).first()
        if sheet:
            records = AttendanceRecord.objects.filter(sheet=sheet).select_related('student')
            records_by_student = {r.student_id: r for r in records}

    active_tab = request.GET.get('tab', 'asignaturas')

    context = {
        'section': section,
        'current_year': current_year,
        'active_period': active_period,
        'my_assignments': my_assignments,
        'principales': principales,
        'humanisticas': humanisticas,
        'arte_deporte': arte_deporte,
        'curriculum': curriculum,
        'active_enrollments': active_enrollments,
        'current_date': current_date,
        'sheet': sheet,
        'records_by_student': records_by_student,
        'first_subject': first_subj,
        'active_tab': active_tab,
    }
    return render(request, 'teachers/course_workspace.html', context)


@login_required
def add_subject_norm_view(request, subject_id):
    """
    Permite asociar una Norma, Estándar MEN o Competencia a una Asignatura / Módulo.
    """
    from apps.subjects.models import Subject, SubjectNorm

    subject = get_object_or_404(Subject, id=subject_id)
    if request.method == 'POST':
        code = request.POST.get('code', '').strip()
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        order = request.POST.get('order', 1)

        if code and title and description:
            try:
                order_val = int(order)
            except ValueError:
                order_val = 1

            SubjectNorm.objects.create(
                subject=subject,
                code=code,
                title=title,
                description=description,
                order=order_val
            )
            messages.success(request, f'Norma/Competencia "{code}" asociada correctamente a {subject.name}.')
        else:
            messages.error(request, 'Todos los campos de la norma son obligatorios.')

    return redirect(request.META.get('HTTP_REFERER', 'teachers:my_courses'))


