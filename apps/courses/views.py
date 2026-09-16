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
    Muestra años lectivos, grados escolares y cursos/grupos activos.
    """
    current_year = get_current_academic_year()
    years = AcademicYear.objects.all()
    grades = GradeLevel.objects.all()
    teachers = CustomUser.objects.filter(role=CustomUser.Role.TEACHER, is_active=True)

    selected_year_id = request.GET.get('year')
    if selected_year_id:
        active_year = get_object_or_404(AcademicYear, id=selected_year_id)
    else:
        active_year = current_year or years.first()

    sections = CourseSection.objects.filter(academic_year=active_year).select_related('grade_level', 'homeroom_teacher') if active_year else []

    context = {
        'current_year': current_year,
        'active_year': active_year,
        'years': years,
        'grades': grades,
        'teachers': teachers,
        'sections': sections,
    }
    return render(request, 'courses/academic_structure.html', context)

@login_required
def sections_partial(request):
    """
    Endpoint HTMX para búsqueda y filtrado reactivo de secciones escolares.
    """
    year_id = request.GET.get('year')
    grade_id = request.GET.get('grade')
    query = request.GET.get('q', '').strip()

    sections = CourseSection.objects.select_related('grade_level', 'academic_year', 'homeroom_teacher').all()

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
