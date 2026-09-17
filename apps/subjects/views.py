from decimal import Decimal
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from .models import KnowledgeArea, Subject, GradeSubject
from apps.courses.models import GradeLevel

@login_required
def curriculum_view(request):
    """
    Vista de la malla curricular escolar e intensidades horarias.
    Acceso exclusivo para profesores (bloqueado para alumnos, padres de familia y secretarias).
    Garantiza que todos los cursos y asignaturas tengan configurada su intensidad horaria.
    """
    if request.user.is_student or request.user.is_parent or request.user.is_secretary:
        raise PermissionDenied("Acceso denegado: La Malla Curricular es de acceso exclusivo para profesores.")
    if not (request.user.is_teacher or request.user.is_admin_role or request.user.is_rector):
        raise PermissionDenied("Acceso denegado: La Malla Curricular es de acceso exclusivo para profesores.")

    areas = KnowledgeArea.objects.prefetch_related('subjects').all()
    grades = GradeLevel.objects.all().order_by('order')
    selected_grade_id = request.GET.get('grade')

    if selected_grade_id:
        active_grade = get_object_or_404(GradeLevel, id=selected_grade_id)
    else:
        active_grade = grades.first()

    # Garantizar que todas las asignaturas tengan intensidad horaria en el grado activo
    if active_grade:
        existing_sub_ids = set(
            GradeSubject.objects.filter(grade_level=active_grade).values_list('subject_id', flat=True)
        )
        all_subjects = Subject.objects.all()
        to_create = []
        for s in all_subjects:
            if s.id not in existing_sub_ids:
                hours = 4
                code_upper = (s.code or '').upper()
                name_upper = (s.name or '').upper()
                if 'MAT' in code_upper or 'ALGEBRA' in name_upper or 'MATEMÁTICAS' in name_upper:
                    hours = 5
                elif 'ESP' in code_upper or 'LENGUA' in name_upper or 'LENGUAJE' in name_upper:
                    hours = 5
                elif 'ING' in code_upper or 'INGLÉS' in name_upper:
                    hours = 3
                elif 'CN' in code_upper or 'CIENCIAS' in name_upper or 'BIOLOGÍA' in name_upper:
                    hours = 4
                elif 'CS' in code_upper or 'SOCIALES' in name_upper or 'HISTORIA' in name_upper:
                    hours = 4
                elif 'EF' in code_upper or 'FÍSICA' in name_upper:
                    hours = 2
                elif 'ART' in code_upper or 'ARTE' in name_upper:
                    hours = 2
                elif 'ETI' in code_upper or 'ÉTICA' in name_upper or 'REL' in code_upper:
                    hours = 1
                to_create.append(GradeSubject(
                    grade_level=active_grade,
                    subject=s,
                    weekly_hours=hours,
                    weight_percentage=Decimal('100.00')
                ))
        if to_create:
            GradeSubject.objects.bulk_create(to_create, ignore_conflicts=True)

    grade_subjects = GradeSubject.objects.filter(
        grade_level=active_grade
    ).select_related('subject', 'subject__area').order_by('subject__area__order', 'subject__name') if active_grade else []

    context = {
        'areas': areas,
        'grades': grades,
        'active_grade': active_grade,
        'grade_subjects': grade_subjects,
    }
    return render(request, 'subjects/curriculum.html', context)

@login_required
def subjects_by_grade_partial(request):
    """
    Endpoint HTMX que retorna opciones <option> de asignaturas pertenecientes a un grado escolar.
    Utilizado en modales de asignación docente.
    """
    grade_id = request.GET.get('grade_id')
    subjects = []
    if grade_id:
        subjects = Subject.objects.filter(curriculum_grades__grade_level_id=grade_id).distinct()
    else:
        subjects = Subject.objects.all()

    return render(request, 'subjects/partials/subject_options.html', {'subjects': subjects})
