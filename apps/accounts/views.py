from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .forms import LoginForm, UserProfileForm
from .models import CustomUser
from apps.audit.services import log_audit

def login_view(request):
    """
    Vista de inicio de sesión con soporte para peticiones estándar y HTMX.
    Registra intentos en auditoría inmutable.
    """
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')

    form = LoginForm(request, data=request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            
            # Registrar login en auditoría
            log_audit(
                user=user,
                action='LOGIN',
                table_name='CustomUser',
                record_id=user.id,
                reason='Inicio de sesión exitoso en la plataforma',
                request=request
            )

            messages.success(request, f'¡Bienvenido a ACADEMIX, {user.get_full_name() or user.username}!')
            
            # Si la petición viene de HTMX, enviamos cabecera de redirección
            if request.headers.get('HX-Request'):
                response = HttpResponse(status=200)
                response['HX-Redirect'] = '/dashboard/'
                return response
            
            return redirect('accounts:dashboard')
        else:
            # Registrar intento fallido
            attempted_user = request.POST.get('username', 'Desconocido')
            log_audit(
                user=None,
                action='FAILED_LOGIN',
                table_name='CustomUser',
                record_id=None,
                new_values={'attempted_username': attempted_user},
                reason=f'Intento fallido de autenticación para usuario: {attempted_user}',
                request=request
            )
            messages.error(request, 'Credenciales inválidas. Por favor verifique su usuario y contraseña.')
            
            if request.headers.get('HX-Request'):
                return render(request, 'accounts/partials/login_form.html', {'form': form})

    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    """
    Cierre de sesión seguro con registro de auditoría.
    """
    if request.user.is_authenticated:
        log_audit(
            user=request.user,
            action='LOGOUT',
            table_name='CustomUser',
            record_id=request.user.id,
            reason='Cierre de sesión manual voluntario',
            request=request
        )
        logout(request)
        messages.info(request, 'Has cerrado sesión satisfactoriamente.')
    return redirect('accounts:login')

@login_required
def dashboard_view(request):
    """
    Dashboard central adaptativo por rol.
    Enriquece el contexto con métricas reales del sistema completo.
    """
    from apps.audit.models import AuditLog
    from apps.courses.models import AcademicYear, CourseSection
    from apps.students.models import Enrollment, StudentProfile
    from apps.teachers.models import TeacherProfile, TeachingAssignment
    from apps.attendance.models import AttendanceRecord
    from apps.grades.models import PeriodFinalGrade
    from apps.alerts.models import SystemAlert
    from apps.homework.models import Homework, HomeworkSubmission
    from apps.periods.models import AcademicPeriod
    from apps.courses.services import get_current_academic_year
    from apps.periods.services import get_current_active_period

    user = request.user
    role = user.role

    current_year = get_current_academic_year()
    active_period = get_current_active_period(current_year) if current_year else None

    # Métricas base siempre calculadas
    total_users = CustomUser.objects.count()
    total_students_qs = CustomUser.objects.filter(role=CustomUser.Role.STUDENT)
    total_teachers_qs = CustomUser.objects.filter(role=CustomUser.Role.TEACHER)

    stats = {
        'total_users': total_users,
        'active_students': total_students_qs.count(),
        'active_teachers': total_teachers_qs.count(),
        'current_year': current_year,
        'active_period': active_period,
        'active_alerts': SystemAlert.objects.filter(is_active=True).count(),
        'audit_events_today': AuditLog.objects.filter(
            timestamp__date=__import__('django').utils.timezone.now().date()
        ).count(),
        'total_sections': CourseSection.objects.filter(
            academic_year=current_year).count() if current_year else 0,
        'total_periods': AcademicPeriod.objects.filter(
            academic_year=current_year).count() if current_year else 0,
    }

    # Métricas específicas por rol
    if user.is_teacher:
        teacher = getattr(user, 'teacher_profile', None)
        if teacher:
            my_assignments = TeachingAssignment.objects.filter(
                teacher=teacher, academic_year=current_year, is_active=True
            ).select_related('course_section', 'subject')
            my_sections_ids = my_assignments.values_list('course_section_id', flat=True).distinct()
            enrolled_in_my_sections = Enrollment.objects.filter(
                course_section_id__in=my_sections_ids,
                academic_year=current_year,
                status=Enrollment.Status.ACTIVE
            ).count()
            pending_homework = Homework.objects.filter(
                teacher=teacher,
                academic_period=active_period,
                is_active=True
            ).count()
            stats['my_assignments_count'] = my_assignments.count()
            stats['my_sections_count'] = my_sections_ids.count()
            stats['enrolled_in_my_sections'] = enrolled_in_my_sections
            stats['pending_homework'] = pending_homework
            stats['my_assignments_list'] = my_assignments[:8]
        else:
            stats['my_assignments_count'] = 0
            stats['my_sections_count'] = 0
            stats['enrolled_in_my_sections'] = 0
            stats['pending_homework'] = 0
            stats['my_assignments_list'] = []

    elif user.is_student:
        student = getattr(user, 'student_profile', None)
        enrollment = None
        my_grades = []
        period_avg = None
        failed_count = 0
        pending_submissions = 0

        if student:
            enrollment = Enrollment.objects.filter(
                student=student, academic_year=current_year
            ).select_related('course_section__grade_level').first()
            if active_period:
                my_grades = PeriodFinalGrade.objects.filter(
                    student=student, academic_period=active_period
                )
            if my_grades:
                scores = [g.final_score for g in my_grades]
                from decimal import Decimal, ROUND_HALF_UP
                period_avg = (sum(scores) / Decimal(str(len(scores)))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
                failed_count = sum(1 for g in my_grades if not g.is_approved)
            if enrollment:
                pending_submissions = HomeworkSubmission.objects.filter(
                    student=student, submitted_at__isnull=True
                ).count()

        # Actividades institucionales próximas dirigidas a estudiantes
        from apps.alerts.models import InstitutionalActivity
        from datetime import date as date_cls
        upcoming_activities = InstitutionalActivity.objects.filter(
            is_active=True,
            event_date__gte=date_cls.today(),
            target_audience__in=['ALL', 'STUDENTS']
        ).order_by('event_date', 'event_time')[:5]

        # Notificaciones activas del estudiante
        from django.db.models import Q as _Q
        student_notifications = SystemAlert.objects.filter(
            is_active=True
        ).filter(
            _Q(target_role='STUDENT') |
            _Q(recipient_user=user) |
            _Q(recipient_user__isnull=True, target_role__isnull=True)
        ).order_by('-created_at')[:5]

        stats['enrollment'] = enrollment
        stats['period_avg'] = period_avg
        stats['failed_count'] = failed_count
        stats['grades_count'] = len(list(my_grades)) if my_grades else 0
        stats['pending_submissions'] = pending_submissions
        stats['upcoming_activities'] = upcoming_activities
        stats['student_notifications'] = student_notifications


    elif user.is_parent:
        # Acudientes: hijos a cargo
        dependents = StudentProfile.objects.filter(parent=user).select_related('user')
        stats['dependents'] = dependents
        stats['dependents_count'] = dependents.count()

    elif user.is_admin_role or user.is_rector:
        # Estadísticas ejecutivas completas
        active_enrollments = Enrollment.objects.filter(
            academic_year=current_year, status=Enrollment.Status.ACTIVE
        ).count() if current_year else 0
        period_grades_count = PeriodFinalGrade.objects.filter(
            academic_period=active_period
        ).count() if active_period else 0
        recent_audit = AuditLog.objects.select_related('user').order_by('-timestamp')[:6]
        stats['active_enrollments'] = active_enrollments
        stats['period_grades_count'] = period_grades_count
        stats['recent_audit'] = recent_audit
        stats['closed_periods'] = AcademicPeriod.objects.filter(
            academic_year=current_year,
            status__in=['CLOSED', 'LOCKED']
        ).count() if current_year else 0
        stats['pending_alerts'] = SystemAlert.objects.filter(
            is_active=True, level='WARNING'
        ).count()

    elif user.is_secretary:
        pending_enrollments = Enrollment.objects.filter(
            academic_year=current_year
        ).count() if current_year else 0
        stats['pending_enrollments'] = pending_enrollments
        stats['total_sections'] = CourseSection.objects.filter(
            academic_year=current_year).count() if current_year else 0

    context = {
        'user': user,
        'role': role,
        'role_display': user.get_role_display(),
        'role_badge': user.get_role_badge_class(),
        'stats': stats,
    }
    return render(request, 'dashboard/index.html', context)


@login_required
def profile_view(request):
    """
    Vista y edición de perfil del usuario con actualización reactiva HTMX.
    """
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            old_data = {'phone': user.phone, 'address': user.address, 'email': user.email}
            form.save()
            new_data = {'phone': user.phone, 'address': user.address, 'email': user.email}
            
            log_audit(
                user=user,
                action='UPDATE',
                table_name='CustomUser',
                record_id=user.id,
                old_values=old_data,
                new_values=new_data,
                reason='Actualización de datos personales de perfil',
                request=request
            )
            messages.success(request, 'Perfil actualizado correctamente.')
            if request.headers.get('HX-Request'):
                return render(request, 'accounts/partials/profile_card.html', {'user': user, 'form': form})
    else:
        form = UserProfileForm(instance=user)

    return render(request, 'accounts/profile.html', {'form': form, 'user': user})
