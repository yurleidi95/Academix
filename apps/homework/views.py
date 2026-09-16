from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import Homework, HomeworkSubmission
from .services import create_homework, submit_homework, grade_submission
from apps.courses.models import CourseSection
from apps.subjects.models import Subject
from apps.periods.models import AcademicPeriod
from apps.courses.services import get_current_academic_year
from apps.periods.services import get_current_active_period
from apps.teachers.models import TeachingAssignment
from apps.students.models import Enrollment

@login_required
def homework_index_view(request):
    """
    Panel de tareas escolares adaptado según el rol (Docente / Estudiante / Directivo).
    """
    current_year = get_current_academic_year()
    active_period = get_current_active_period(current_year) if current_year else None
    user = request.user

    if user.is_teacher and hasattr(user, 'teacher_profile'):
        homeworks = Homework.objects.filter(
            teacher=user.teacher_profile,
            academic_period=active_period
        ).select_related('course_section', 'subject').order_by('-due_date')
        assignments = TeachingAssignment.objects.filter(teacher=user.teacher_profile, is_active=True)
    elif user.is_student and hasattr(user, 'student_profile'):
        enrollment = Enrollment.objects.filter(student=user.student_profile, academic_year=current_year, status=Enrollment.Status.ACTIVE).first()
        if enrollment:
            homeworks = Homework.objects.filter(
                course_section=enrollment.course_section,
                academic_period=active_period,
                is_active=True
            ).select_related('subject', 'teacher__user').order_by('due_date')
        else:
            homeworks = Homework.objects.none()
        assignments = []
    else:
        homeworks = Homework.objects.filter(academic_period=active_period).select_related('course_section', 'subject', 'teacher__user') if active_period else []
        assignments = []

    # Mapear entregas del estudiante si es alumno
    student_submissions = {}
    if user.is_student and hasattr(user, 'student_profile'):
        subs = HomeworkSubmission.objects.filter(student=user.student_profile)
        for s in subs:
            student_submissions[s.homework_id] = s
        for hw in homeworks:
            hw.my_submission = student_submissions.get(hw.id)


    sections = CourseSection.objects.filter(academic_year=current_year) if current_year else []
    subjects = Subject.objects.all()

    context = {
        'current_year': current_year,
        'active_period': active_period,
        'homeworks': homeworks,
        'student_submissions': student_submissions,
        'assignments': assignments,
        'sections': sections,
        'subjects': subjects,
    }
    return render(request, 'homework/index.html', context)

@login_required
def create_homework_view(request):
    """
    Crea una nueva tarea escolar asignada a un grupo.
    """
    if request.method == 'POST' and (request.user.is_teacher or request.user.is_admin_role):
        section_id = request.POST.get('section_id')
        subject_id = request.POST.get('subject_id')
        title = request.POST.get('title', '').strip()
        description = request.POST.get('description', '').strip()
        due_date_str = request.POST.get('due_date')
        attachment = request.FILES.get('attachment')

        section = get_object_or_404(CourseSection, id=section_id)
        subject = get_object_or_404(Subject, id=subject_id)
        current_year = get_current_academic_year()
        active_period = get_current_active_period(current_year)

        teacher_profile = getattr(request.user, 'teacher_profile', None)
        if not teacher_profile:
            assignment = TeachingAssignment.objects.filter(course_section=section, subject=subject).first()
            teacher_profile = assignment.teacher if assignment else None

        if not teacher_profile:
            messages.error(request, 'No se pudo identificar el docente titular para esta tarea.')
            return redirect('homework:index')

        try:
            create_homework(
                teacher=teacher_profile,
                course_section=section,
                subject=subject,
                academic_period=active_period,
                title=title,
                description=description,
                due_date=due_date_str,
                attachment=attachment,
                user=request.user
            )
            messages.success(request, f'Tarea "{title}" publicada con éxito para {section.name}.')
        except Exception as e:
            messages.error(request, f'Error al publicar tarea: {str(e)}')

    return redirect('homework:index')

@login_required
def submit_homework_view(request, homework_id):
    """
    Registra la entrega de la tarea por parte del estudiante.
    """
    if request.method == 'POST' and request.user.is_student:
        homework = get_object_or_404(Homework, id=homework_id)
        student_profile = request.user.student_profile
        submission_text = request.POST.get('submission_text', '').strip()
        attachment = request.FILES.get('attachment')

        try:
            submit_homework(
                homework=homework,
                student=student_profile,
                submission_text=submission_text,
                attachment=attachment,
                user=request.user
            )
            messages.success(request, f'¡Tu tarea "{homework.title}" fue enviada satisfactoriamente!')
        except Exception as e:
            messages.error(request, f'Error al enviar la tarea: {str(e)}')

    return redirect('homework:index')

@login_required
def grade_submission_view(request, submission_id):
    """
    Califica y retroalimenta la entrega de una tarea.
    """
    if request.method == 'POST' and (request.user.is_teacher or request.user.is_admin_role):
        score = request.POST.get('score')
        feedback = request.POST.get('feedback', '').strip()

        try:
            grade_submission(submission_id, score, feedback=feedback, user=request.user)
            messages.success(request, 'Calificación de tarea registrada con éxito.')
        except Exception as e:
            messages.error(request, f'Error al calificar tarea: {str(e)}')

    return redirect('homework:index')
