import csv
import io
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Avg
from apps.courses.models import CourseSection
from apps.subjects.models import Subject, KnowledgeArea
from apps.periods.models import AcademicPeriod
from apps.students.models import StudentProfile, Enrollment
from apps.teachers.models import TeachingAssignment
from apps.grades.models import EvaluationCriterion, GradeRecord, PeriodFinalGrade
from apps.attendance.models import AttendanceRecord

def build_student_bulletin_data(student, section, period):
    """
    Construye la estructura completa de datos del Boletín Oficial de Calificaciones
    de un estudiante conforme al Decreto 1290 y las áreas del plan de estudios.
    """
    academic_year = section.academic_year
    enrollment = Enrollment.objects.filter(
        student=student,
        course_section=section,
        academic_year=academic_year
    ).first()

    # Director de grupo o docente titular principal
    assignment_director = TeachingAssignment.objects.filter(
        course_section=section,
        academic_year=academic_year,
        is_active=True
    ).select_related('teacher__user').first()
    group_director = assignment_director.teacher if assignment_director else None

    # Áreas de conocimiento y asignaturas
    areas = KnowledgeArea.objects.all().order_by('name')
    bulletin_areas = []

    total_weighted_score = Decimal('0.00')
    total_subjects_count = 0
    total_failed_count = 0
    total_absences_period = 0

    for area in areas:
        area_subjects = Subject.objects.filter(area=area).order_by('name')
        subject_items = []
        area_score_sum = Decimal('0.00')
        area_sub_count = 0

        for sub in area_subjects:
            assignment = TeachingAssignment.objects.filter(
                course_section=section,
                subject=sub,
                academic_year=academic_year,
                is_active=True
            ).select_related('teacher__user').first()

            # Solo incluir asignaturas que tengan asignación o notas en esta sección
            final_grade = PeriodFinalGrade.objects.filter(
                student=student,
                course_section=section,
                subject=sub,
                academic_period=period
            ).first()

            if not assignment and not final_grade:
                continue

            # Criterios y notas
            criteria = EvaluationCriterion.objects.filter(
                course_section=section,
                subject=sub,
                academic_period=period
            ).order_by('order')

            criteria_details = []
            feedback_notes = []
            for crit in criteria:
                rec = GradeRecord.objects.filter(
                    student=student,
                    course_section=section,
                    subject=sub,
                    academic_period=period,
                    criterion=crit
                ).first()
                sc = rec.score if rec else Decimal('1.00')
                if rec and rec.feedback:
                    feedback_notes.append(rec.feedback)
                criteria_details.append({
                    'name': crit.name,
                    'percentage': crit.percentage,
                    'score': sc
                })

            # Faltas en el periodo
            absences = AttendanceRecord.objects.filter(
                student=student,
                session__course_section=section,
                session__subject=sub,
                session__academic_period=period
            )
            unjustified_abs = absences.filter(status=AttendanceRecord.Status.UNJUSTIFIED).count()
            justified_abs = absences.filter(status=AttendanceRecord.Status.JUSTIFIED).count()
            total_absences_period += (unjustified_abs + justified_abs)

            score_val = final_grade.final_score if final_grade else Decimal('1.00')
            is_approved = final_grade.is_approved if final_grade else (score_val >= Decimal('3.00'))
            perf_level = final_grade.get_performance_level_display() if final_grade else 'Bajo'

            if not is_approved:
                total_failed_count += 1

            total_weighted_score += score_val
            total_subjects_count += 1
            area_score_sum += score_val
            area_sub_count += 1

            subject_items.append({
                'subject': sub,
                'teacher': assignment.teacher if assignment else None,
                'criteria': criteria_details,
                'final_score': score_val,
                'performance_level': perf_level,
                'is_approved': is_approved,
                'unjustified_abs': unjustified_abs,
                'justified_abs': justified_abs,
                'feedback': " | ".join(feedback_notes) if feedback_notes else None,
            })

        if subject_items:
            area_avg = (area_score_sum / Decimal(str(area_sub_count))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            bulletin_areas.append({
                'area': area,
                'subjects': subject_items,
                'area_average': area_avg,
            })

    # Promedio general del estudiante en el periodo
    if total_subjects_count > 0:
        period_average = (total_weighted_score / Decimal(str(total_subjects_count))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
    else:
        period_average = Decimal('1.00')

    # Cálculo del puesto (ranking) en la sección
    ranking_data = calculate_section_ranking(section, period)
    student_rank = ranking_data.get(student.id, {'rank': 1, 'total': len(ranking_data)})

    return {
        'student': student,
        'enrollment': enrollment,
        'section': section,
        'period': period,
        'academic_year': academic_year,
        'group_director': group_director,
        'bulletin_areas': bulletin_areas,
        'period_average': period_average,
        'student_rank': student_rank['rank'],
        'total_students_section': student_rank['total'],
        'total_subjects_count': total_subjects_count,
        'total_failed_count': total_failed_count,
        'total_absences_period': total_absences_period,
    }

def calculate_section_ranking(section, period):
    """
    Calcula los promedios de todos los alumnos de la sección en el periodo y asigna los puestos ordenados.
    """
    enrollments = Enrollment.objects.filter(
        course_section=section,
        academic_year=section.academic_year,
        status=Enrollment.Status.ACTIVE
    ).select_related('student')

    student_averages = []
    for enr in enrollments:
        grades = PeriodFinalGrade.objects.filter(
            student=enr.student,
            course_section=section,
            academic_period=period
        )
        if grades.exists():
            avg_score = sum([g.final_score for g in grades]) / Decimal(str(grades.count()))
            avg_dec = avg_score.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        else:
            avg_dec = Decimal('1.00')
        student_averages.append({
            'student_id': enr.student.id,
            'average': avg_dec
        })

    # Ordenar descendente por promedio
    student_averages.sort(key=lambda x: x['average'], reverse=True)

    ranking_map = {}
    total_count = len(student_averages)
    for idx, item in enumerate(student_averages, start=1):
        ranking_map[item['student_id']] = {
            'rank': idx,
            'total': total_count,
            'average': item['average']
        }

    return ranking_map

def build_section_consolidated_data(section, period):
    """
    Genera la sábana consolidada de calificaciones de todo el grupo para el periodo.
    """
    academic_year = section.academic_year
    enrollments = Enrollment.objects.filter(
        course_section=section,
        academic_year=academic_year,
        status=Enrollment.Status.ACTIVE
    ).select_related('student__user').order_by('student__user__last_name', 'student__user__first_name')

    # Asignaturas de la sección
    assignments = TeachingAssignment.objects.filter(
        course_section=section,
        academic_year=academic_year,
        is_active=True
    ).select_related('subject')
    subjects = list(dict.fromkeys([a.subject for a in assignments]))
    if not subjects:
        # Fallback a materias con notas en esta sección
        sub_ids = PeriodFinalGrade.objects.filter(course_section=section, academic_period=period).values_list('subject_id', flat=True).distinct()
        subjects = list(Subject.objects.filter(id__in=sub_ids).order_by('name'))

    ranking_map = calculate_section_ranking(section, period)

    rows = []
    for enr in enrollments:
        st = enr.student
        scores = {}
        scores_list = []
        failed_count = 0
        for sub in subjects:
            rec = PeriodFinalGrade.objects.filter(
                student=st,
                course_section=section,
                subject=sub,
                academic_period=period
            ).first()
            if rec:
                item_data = {
                    'subject': sub,
                    'score': rec.final_score,
                    'is_approved': rec.is_approved,
                    'badge': rec.badge_class
                }
                scores[sub.id] = item_data
                scores_list.append(item_data)
                if not rec.is_approved:
                    failed_count += 1
            else:
                item_data = {
                    'subject': sub,
                    'score': Decimal('1.00'),
                    'is_approved': False,
                    'badge': 'bg-danger text-white'
                }
                scores[sub.id] = item_data
                scores_list.append(item_data)
                failed_count += 1

        rank_info = ranking_map.get(st.id, {'rank': '-', 'average': Decimal('1.00')})
        rows.append({
            'student': st,
            'scores': scores,
            'scores_list': scores_list,
            'average': rank_info['average'],
            'rank': rank_info['rank'],
            'failed_count': failed_count,
        })

    # Ordenar filas por puesto
    rows.sort(key=lambda r: (r['rank'] if isinstance(r['rank'], int) else 999))

    return {
        'section': section,
        'period': period,
        'subjects': subjects,
        'rows': rows,
        'total_students': len(rows),
    }

def export_consolidated_csv(section, period):
    """
    Exporta la sábana consolidada en formato CSV con codificación UTF-8 con BOM.
    """
    data = build_section_consolidated_data(section, period)
    output = io.StringIO()
    # Escribir UTF-8 BOM
    output.write('\ufeff')
    writer = csv.writer(output, dialect='excel')

    # Encabezados
    headers = ['Puesto', 'Código Estudiantil', 'Apellidos y Nombres', 'Documento']
    for sub in data['subjects']:
        headers.append(f"{sub.code} ({sub.name})")
    headers.extend(['Promedio General', 'Asignaturas Reprobadas'])
    writer.writerow(headers)

    # Filas
    for row in data['rows']:
        st = row['student']
        line = [
            row['rank'],
            st.student_code,
            st.user.get_full_name() or st.user.username,
            st.user.document_number or ''
        ]
        for sub in data['subjects']:
            score_data = row['scores'].get(sub.id)
            line.append(str(score_data['score']) if score_data else '1.00')
        line.append(str(row['average']))
        line.append(row['failed_count'])
        writer.writerow(line)

    return output.getvalue()

def build_honor_roll_data(section, period):
    """
    Genera el Cuadro de Honor (Top 5 estudiantes) y estadísticas generales de aprobación.
    """
    consolidated = build_section_consolidated_data(section, period)
    rows = consolidated['rows']

    # Top 5 con promedios >= 3.80
    honor_students = [r for r in rows if r['average'] >= Decimal('3.80')][:5]

    total = len(rows)
    passed_all = len([r for r in rows if r['failed_count'] == 0])
    passed_rate = ((Decimal(str(passed_all)) / Decimal(str(total))) * Decimal('100.00')).quantize(Decimal('0.1'), rounding=ROUND_HALF_UP) if total > 0 else Decimal('0.0')

    # Detección de asignaturas críticas (con mayor número de reprobados)
    subject_failed_counts = {}
    for sub in consolidated['subjects']:
        failed_in_sub = sum([1 for r in rows if not r['scores'].get(sub.id, {}).get('is_approved', True)])
        subject_failed_counts[sub] = failed_in_sub

    critical_subjects = sorted(subject_failed_counts.items(), key=lambda x: x[1], reverse=True)[:3]

    return {
        'section': section,
        'period': period,
        'honor_students': honor_students,
        'total_students': total,
        'passed_all_count': passed_all,
        'approval_rate': passed_rate,
        'critical_subjects': critical_subjects,
    }
