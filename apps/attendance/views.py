from datetime import date
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import AttendanceSession, AttendanceRecord
from .services import (
    get_or_create_attendance_session,
    update_student_attendance,
    mark_all_session_present,
    calculate_student_absence_stats
)
from apps.courses.models import CourseSection
from apps.subjects.models import Subject
from apps.teachers.models import TeachingAssignment
from apps.students.models import Enrollment
from apps.courses.services import get_current_academic_year
from apps.periods.services import get_current_active_period

@login_required
def attendance_index_view(request):
    """
    Selector inicial de curso, asignatura y fecha para toma o consulta de asistencia.
    Si el usuario es estudiante, muestra directamente su historial y semáforo personal.
    """
    current_year = get_current_academic_year()
    active_period = get_current_active_period(current_year) if current_year else None
    today = date.today()

    # 1. Modo Estudiante: Consulta segura de su propia asistencia y semáforo
    if request.user.is_student:
        student = getattr(request.user, 'student_profile', None)
        enrollment = Enrollment.objects.filter(
            student=student,
            academic_year=current_year,
            status=Enrollment.Status.ACTIVE
        ).select_related('course_section__grade_level').first() if student else None

        attendance_by_subject = []
        recent_records = []
        if student and active_period:
            from apps.subjects.models import Subject
            subjects = Subject.objects.all()
            for subj in subjects:
                stats = calculate_student_absence_stats(student, subj, active_period)
                if stats['total_sessions'] > 0:
                    attendance_by_subject.append({
                        'subject': subj,
                        'stats': stats,
                    })

            recent_records = AttendanceRecord.objects.filter(
                student=student,
                session__academic_period=active_period
            ).select_related('session__subject').order_by('-session__date')[:15]

        return render(request, 'attendance/student_attendance.html', {
            'enrollment': enrollment,
            'current_year': current_year,
            'active_period': active_period,
            'attendance_by_subject': attendance_by_subject,
            'recent_records': recent_records,
        })

    # 2. Modo Docente / Directivo / Secretaría
    if request.user.is_teacher and hasattr(request.user, 'teacher_profile'):
        assignments = TeachingAssignment.objects.filter(
            teacher=request.user.teacher_profile,
            academic_year=current_year,
            is_active=True
        ).select_related('course_section', 'subject')
        sections = CourseSection.objects.filter(id__in=assignments.values_list('course_section_id', flat=True))
    else:
        assignments = TeachingAssignment.objects.filter(academic_year=current_year, is_active=True).select_related('course_section', 'subject')
        sections = CourseSection.objects.filter(academic_year=current_year).select_related('grade_level') if current_year else []

    context = {
        'current_year': current_year,
        'active_period': active_period,
        'today': today.isoformat(),
        'sections': sections,
        'assignments': assignments,
    }
    return render(request, 'attendance/index.html', context)

@login_required
def attendance_sheet_view(request):
    """
    Planilla interactiva de llamado de lista.
    Estudiantes tienen prohibido el acceso a la lista grupal.
    Secretaría tiene acceso de solo lectura.
    Docentes solo pueden pasar lista de sus asignaciones.
    """
    if request.user.is_student or request.user.is_parent:
        messages.error(request, 'No está autorizado para consultar la lista de clase de otros estudiantes.')
        return redirect('attendance:index')

    section_id = request.GET.get('section_id')
    subject_id = request.GET.get('subject_id')
    session_date_str = request.GET.get('date', date.today().isoformat())

    try:
        session_date = date.fromisoformat(session_date_str)
    except (ValueError, TypeError):
        session_date = date.today()

    if not section_id or not subject_id:
        messages.warning(request, 'Por favor seleccione un grupo y una asignatura.')
        return redirect('attendance:index')

    section = get_object_or_404(CourseSection, id=section_id)
    subject = get_object_or_404(Subject, id=subject_id)

    # Validar permisos de edición: Secretaría es solo lectura
    is_editable = True
    if request.user.is_secretary:
        is_editable = False
    elif request.user.is_teacher and hasattr(request.user, 'teacher_profile'):
        has_assignment = TeachingAssignment.objects.filter(
            teacher=request.user.teacher_profile,
            course_section=section,
            subject=subject,
            academic_year=section.academic_year,
            is_active=True
        ).exists()
        if not has_assignment and not (request.user.is_admin_role or request.user.is_rector):
            is_editable = False

    try:
        session = get_or_create_attendance_session(
            course_section=section,
            subject=subject,
            session_date=session_date,
            recorded_by=request.user
        )
    except Exception as e:
        messages.error(request, f'No se pudo abrir la planilla: {str(e)}')
        return redirect('attendance:index')

    if not session.academic_period.is_editable:
        is_editable = False

    # Enriquecer cada registro con sus estadísticas de ausentismo acumuladas
    records = session.records.select_related('student__user', 'student__parent').all()
    enriched_records = []
    for r in records:
        stats = calculate_student_absence_stats(r.student, subject, session.academic_period)
        enriched_records.append({
            'record': r,
            'student': r.student,
            'stats': stats,
        })

    context = {
        'session': session,
        'section': section,
        'subject': subject,
        'session_date': session_date,
        'enriched_records': enriched_records,
        'is_editable': is_editable,
    }
    return render(request, 'attendance/sheet.html', context)

@login_required
def update_record_inline_view(request, record_id):
    """
    Endpoint HTMX para guardado en línea (Inline Edit) del estado de asistencia de un alumno.
    Control estricto: Secretaría y Estudiantes no pueden modificar asistencia.
    """
    if not (request.user.is_teacher or request.user.is_admin_role or request.user.is_rector):
        return HttpResponse('<div class="text-danger small fw-bold">No tiene permisos para modificar asistencia.</div>', status=403)

    record = get_object_or_404(AttendanceRecord.objects.select_related('session__academic_period', 'session__subject', 'student__user'), id=record_id)
    new_status = request.POST.get('status')
    justification = request.POST.get('justification', '').strip()

    if new_status in AttendanceRecord.Status.values:
        try:
            record, stats = update_student_attendance(
                session=record.session,
                student=record.student,
                new_status=new_status,
                justification=justification or None,
                user=request.user
            )
        except Exception as e:
            return HttpResponse(f'<div class="text-danger small">{str(e)}</div>', status=400)

        context = {
            'r': {
                'record': record,
                'student': record.student,
                'stats': stats,
            },
            'session': record.session,
            'is_editable': record.session.academic_period.is_editable and not request.user.is_secretary,
        }
        return render(request, 'attendance/partials/record_row.html', context)

    return HttpResponse(status=400)

@login_required

def mark_all_present_view(request, session_id):
    """
    Endpoint HTMX para marcar a todos los alumnos como PRESENTES de manera masiva.
    """
    session = get_object_or_404(AttendanceSession, id=session_id)
    try:
        mark_all_session_present(session, user=request.user)
    except Exception as e:
        messages.error(request, f'Error al actualizar: {str(e)}')

    records = session.records.select_related('student__user', 'student__parent').all()
    enriched_records = []
    for r in records:
        stats = calculate_student_absence_stats(r.student, session.subject, session.academic_period)
        enriched_records.append({
            'record': r,
            'student': r.student,
            'stats': stats,
        })

    context = {
        'session': session,
        'enriched_records': enriched_records,
        'is_editable': session.academic_period.is_editable,
    }
    return render(request, 'attendance/partials/sheet_table.html', context)
