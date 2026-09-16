from decimal import Decimal, ROUND_HALF_UP
from django.utils import timezone
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Homework, HomeworkSubmission
from apps.audit.services import log_audit

@transaction.atomic
def create_homework(teacher, course_section, subject, academic_period, title, description, due_date, attachment=None, user=None):
    """
    Publica una nueva actividad o tarea escolar para el grupo.
    """
    hw = Homework.objects.create(
        teacher=teacher,
        course_section=course_section,
        subject=subject,
        academic_period=academic_period,
        title=title,
        description=description,
        due_date=due_date,
        attachment=attachment
    )

    log_audit(
        action='INSERT',
        table_name='Homework',
        record_id=hw.id,
        new_values={'title': title, 'section': course_section.name, 'subject': subject.code},
        reason=f'Asignación de tarea: {title} para grupo {course_section.name}',
        user=user
    )

    return hw

@transaction.atomic
def submit_homework(homework, student, submission_text=None, attachment=None, user=None):
    """
    Registra o actualiza la entrega de una tarea por parte del estudiante.
    """
    status = HomeworkSubmission.Status.LATE if homework.is_expired else HomeworkSubmission.Status.SUBMITTED

    submission, created = HomeworkSubmission.objects.update_or_create(
        homework=homework,
        student=student,
        defaults={
            'submission_text': submission_text,
            'attachment': attachment,
            'status': status,
        }
    )

    log_audit(
        action='INSERT' if created else 'UPDATE',
        table_name='HomeworkSubmission',
        record_id=submission.id,
        new_values={'student': student.user.username, 'homework': homework.title, 'status': status},
        reason=f'Entrega de tarea {homework.title} por {student.user.username}',
        user=user
    )

    return submission

@transaction.atomic
def grade_submission(submission_id, score, feedback=None, user=None):
    """
    Califica y retroalimenta la entrega de una tarea estudiantil.
    """
    submission = HomeworkSubmission.objects.select_for_update().get(id=submission_id)
    score_dec = Decimal(str(score)).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

    if score_dec < Decimal('0.00') or score_dec > Decimal('10.00'):
        raise ValidationError("La calificación debe encontrarse entre 0.00 y 5.00 (o hasta 10.00).")


    submission.score = score_dec
    if feedback:
        submission.teacher_feedback = feedback
    submission.status = HomeworkSubmission.Status.GRADED
    submission.save()

    log_audit(
        action='UPDATE',
        table_name='HomeworkSubmission',
        record_id=submission.id,
        new_values={'score': str(score_dec), 'feedback': feedback, 'status': 'GRADED'},
        reason=f'Calificación de tarea {submission.homework.title} para {submission.student.user.username}: {score_dec}',
        user=user
    )

    return submission
