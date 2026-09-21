from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import AcademicYear, GradeLevel, CourseSection
from .services import get_current_academic_year, create_course_section
from apps.accounts.models import CustomUser

@login_required
def academic_structure_view(request):
    """
    Vista principal de la estructura académica institucional.
    Muestra años lectivos, grados escolares y cursos/grupos activos de la institución actual.
    """
    from .models import InstitutionSetting
    inst_settings = InstitutionSetting.get_settings()
    inst_type = inst_settings.institution_type

    current_year = get_current_academic_year()
    years = AcademicYear.objects.all()
    grades = GradeLevel.objects.filter(institution_type=inst_type)
    teachers = CustomUser.objects.filter(role=CustomUser.Role.TEACHER, is_active=True)

    selected_year_id = request.GET.get('year')
    if selected_year_id:
        active_year = get_object_or_404(AcademicYear, id=selected_year_id)
    else:
        active_year = current_year or years.first()

    sections = CourseSection.objects.filter(
        academic_year=active_year,
        grade_level__institution_type=inst_type
    ).select_related('grade_level', 'homeroom_teacher') if active_year else []

    context = {
        'current_year': current_year,
        'active_year': active_year,
        'years': years,
        'grades': grades,
        'teachers': teachers,
        'sections': sections,
        'inst_settings': inst_settings,
    }
    return render(request, 'courses/academic_structure.html', context)

@login_required
def sections_partial(request):
    """
    Endpoint HTMX para búsqueda y filtrado reactivo de secciones de la institución activa.
    """
    from .models import InstitutionSetting
    inst_type = InstitutionSetting.get_settings().institution_type

    year_id = request.GET.get('year')
    grade_id = request.GET.get('grade')
    query = request.GET.get('q', '').strip()

    sections = CourseSection.objects.filter(
        grade_level__institution_type=inst_type
    ).select_related('grade_level', 'academic_year', 'homeroom_teacher')

    if year_id:
        sections = sections.filter(academic_year_id=year_id)
    if grade_id:
        sections = sections.filter(grade_level_id=grade_id)
    if query:
        sections = sections.filter(name__icontains=query)

    return render(request, 'courses/partials/sections_table.html', {'sections': sections})

@login_required
def create_section_view(request):
    """
    Crea una nueva sección escolar mediante HTMX o petición tradicional.
    """
    if request.method == 'POST':
        year_id = request.POST.get('academic_year')
        grade_id = request.POST.get('grade_level')
        name = request.POST.get('name', '').strip()
        classroom = request.POST.get('classroom', '').strip()
        teacher_id = request.POST.get('homeroom_teacher') or None
        capacity = int(request.POST.get('capacity', 35))

        academic_year = get_object_or_404(AcademicYear, id=year_id)
        grade_level = get_object_or_404(GradeLevel, id=grade_id)
        teacher = get_object_or_404(CustomUser, id=teacher_id) if teacher_id else None

        try:
            create_course_section(
                academic_year=academic_year,
                grade_level=grade_level,
                name=name,
                classroom=classroom,
                homeroom_teacher=teacher,
                capacity=capacity,
                user=request.user
            )
            messages.success(request, f'Grupo {name} creado con éxito.')
        except Exception as e:
            messages.error(request, f'Error al crear grupo: {str(e)}')

    return redirect('courses:academic_structure')


@login_required
def institution_settings_view(request):
    """
    Panel de configuración institucional y adaptación de terminología.
    Permite parametrizar ACADEMIX para Colegios, Universidades, Institutos Técnicos (SENA) o Academias.
    Accesible para Administrador y Rector.
    """
    if not (request.user.is_admin_role or request.user.is_rector):
        messages.error(request, 'No tiene permisos para modificar los parámetros institucionales.')
        return redirect('dashboard')

    from .models import InstitutionSetting
    settings_obj = InstitutionSetting.get_settings()

    if request.method == 'POST':
        action = request.POST.get('action')

        if action == 'apply_preset':
            preset = request.POST.get('preset')
            if preset in dict(InstitutionSetting.InstitutionType.choices):
                settings_obj.apply_preset(preset)
                messages.success(request, f'Configuración adaptada exitosamente al modo: {settings_obj.get_institution_type_display()}')
            else:
                messages.error(request, 'Preset no válido.')
        else:
            # Actualización manual detallada
            settings_obj.institution_name = request.POST.get('institution_name', settings_obj.institution_name).strip()
            settings_obj.slogan = request.POST.get('slogan', settings_obj.slogan).strip()
            settings_obj.institution_type = request.POST.get('institution_type', settings_obj.institution_type)
            settings_obj.term_student = request.POST.get('term_student', settings_obj.term_student).strip()
            settings_obj.term_students = request.POST.get('term_students', settings_obj.term_students).strip()
            settings_obj.term_teacher = request.POST.get('term_teacher', settings_obj.term_teacher).strip()
            settings_obj.term_teachers = request.POST.get('term_teachers', settings_obj.term_teachers).strip()
            settings_obj.term_grade = request.POST.get('term_grade', settings_obj.term_grade).strip()
            settings_obj.term_section = request.POST.get('term_section', settings_obj.term_section).strip()
            settings_obj.term_sections = request.POST.get('term_sections', settings_obj.term_sections).strip()
            settings_obj.term_subject = request.POST.get('term_subject', settings_obj.term_subject).strip()
            settings_obj.term_subjects = request.POST.get('term_subjects', settings_obj.term_subjects).strip()
            settings_obj.term_director = request.POST.get('term_director', settings_obj.term_director).strip()
            settings_obj.save()
            messages.success(request, 'Parámetros institucionales actualizados correctamente.')

        return redirect('courses:institution_settings')

    context = {
        'inst_settings': settings_obj,
        'institution_types': InstitutionSetting.InstitutionType.choices,
    }
    return render(request, 'courses/institution_settings.html', context)

