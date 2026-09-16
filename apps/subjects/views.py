from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import KnowledgeArea, Subject, GradeSubject
from apps.courses.models import GradeLevel

@login_required
def curriculum_view(request):
    """
    Vista de la malla curricular escolar e intensidades horarias.
    """
    areas = KnowledgeArea.objects.prefetch_related('subjects').all()
    grades = GradeLevel.objects.all()
    selected_grade_id = request.GET.get('grade')

    if selected_grade_id:
        active_grade = get_object_or_404(GradeLevel, id=selected_grade_id)
    else:
        active_grade = grades.first()

    grade_subjects = GradeSubject.objects.filter(grade_level=active_grade).select_related('subject', 'subject__area') if active_grade else []

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
