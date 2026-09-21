import logging
from decimal import Decimal
from django.db import transaction
from apps.courses.models import AcademicYear, GradeLevel, CourseSection, InstitutionSetting
from apps.subjects.models import KnowledgeArea, Subject, GradeSubject
from apps.accounts.models import CustomUser
from apps.teachers.models import TeacherProfile, TeachingAssignment
from apps.students.models import StudentProfile, Enrollment

logger = logging.getLogger(__name__)

def provision_institution_environment(institution_type):
    """
    Aprovisiona automáticamente la estructura, asignaturas, cursos, docentes y alumnos
    específicos para el modelo de institución seleccionado si aún no existen.
    Garantiza aislamiento total para que cada modelo tenga su propio entorno de datos.
    """
    with transaction.atomic():
        # 1. Asegurar año lectivo activo vigente
        current_year, _ = AcademicYear.objects.get_or_create(
            year=2026,
            defaults={
                'name': 'Año Lectivo 2026',
                'start_date': '2026-01-15',
                'end_date': '2026-11-30',
                'status': AcademicYear.Status.ACTIVE,
                'is_current': True
            }
        )
        if not current_year.is_current:
            AcademicYear.objects.filter(is_current=True).update(is_current=False)
            current_year.is_current = True
            current_year.status = AcademicYear.Status.ACTIVE
            current_year.save()

        if institution_type == InstitutionSetting.InstitutionType.SENA_TECNICO:
            _provision_sena(current_year)
        elif institution_type == InstitutionSetting.InstitutionType.UNIVERSIDAD:
            _provision_universidad(current_year)
        elif institution_type == InstitutionSetting.InstitutionType.ACADEMIA:
            _provision_academia(current_year)
        else:
            _provision_colegio(current_year)


def _provision_colegio(year):
    inst_type = InstitutionSetting.InstitutionType.COLEGIO
    # Grados Escolares
    grades_def = [
        ('Sexto', 'GR-06', GradeLevel.LevelStage.SECUNDARIA, 6),
        ('Séptimo', 'GR-07', GradeLevel.LevelStage.SECUNDARIA, 7),
        ('Octavo', 'GR-08', GradeLevel.LevelStage.SECUNDARIA, 8),
        ('Noveno', 'GR-09', GradeLevel.LevelStage.SECUNDARIA, 9),
        ('Décimo', 'GR-10', GradeLevel.LevelStage.MEDIA, 10),
        ('Once', 'GR-11', GradeLevel.LevelStage.MEDIA, 11),
    ]
    grades_dict = {}
    for name, code, stage, order in grades_def:
        g, _ = GradeLevel.objects.get_or_create(
            institution_type=inst_type,
            code=code,
            defaults={'name': name, 'level_stage': stage, 'order': order}
        )
        grades_dict[code] = g

    # Áreas y Asignaturas
    areas_def = [
        ('Matemáticas y Lógica', 1, [
            ('Matemáticas Fundamentales', 'MAT-06', 'Aritmética, álgebra y resolución de problemas.'),
            ('Geometría y Estadística', 'GEO-06', 'Geometría plana y análisis descriptivo de datos.')
        ]),
        ('Lengua Castellana y Humanidades', 2, [
            ('Lengua Castellana', 'CAS-06', 'Comprensión lectora, gramática y producción escrita.'),
            ('Inglés Comunicativo', 'ING-06', 'Nivel básico-intermedio A2 de inglés comunicativo.')
        ]),
        ('Ciencias Naturales y Educación Ambiental', 3, [
            ('Biología General', 'BIO-06', 'Biología celular, ecosistemas y biodiversidad.'),
            ('Física Elemental', 'FIS-10', 'Cinemática, dinámica y leyes de Newton.')
        ]),
        ('Tecnología e Informática', 4, [
            ('Tecnología e Informática', 'TEC-06', 'Herramientas digitales, ofimática y lógica computacional.')
        ]),
    ]
    for area_name, order, subjects in areas_def:
        area, _ = KnowledgeArea.objects.get_or_create(
            institution_type=inst_type,
            name=area_name,
            defaults={'order': order}
        )
        for s_name, s_code, s_desc in subjects:
            subj, _ = Subject.objects.get_or_create(
                institution_type=inst_type,
                code=s_code,
                defaults={'name': s_name, 'area': area, 'description': s_desc}
            )
            # Vincular a grado 6 si no existe
            if 'GR-06' in grades_dict:
                GradeSubject.objects.get_or_create(
                    grade_level=grades_dict['GR-06'],
                    subject=subj,
                    defaults={'weekly_hours': 4, 'weight_percentage': Decimal('100.00')}
                )

    # Cursos
    sections_def = [
        ('6-A', 'GR-06', 'Aula 101', 35),
        ('6-B', 'GR-06', 'Aula 102', 35),
        ('10-A', 'GR-10', 'Aula 201', 35),
    ]
    for sec_name, g_code, classroom, cap in sections_def:
        if g_code in grades_dict:
            CourseSection.objects.get_or_create(
                academic_year=year,
                grade_level=grades_dict[g_code],
                name=sec_name,
                defaults={'classroom': classroom, 'capacity': cap, 'is_active': True}
            )


def _provision_sena(year):
    inst_type = InstitutionSetting.InstitutionType.SENA_TECNICO
    # Niveles / Trimestres
    trimestres_def = [
        ('Trimestre I - Inducción y Fundamentos', 'SENA-TR-1', GradeLevel.LevelStage.TECNICO, 1),
        ('Trimestre II - Desarrollo y Algoritmos', 'SENA-TR-2', GradeLevel.LevelStage.TECNICO, 2),
        ('Trimestre III - Bases de Datos y Backend', 'SENA-TR-3', GradeLevel.LevelStage.TECNICO, 3),
        ('Trimestre IV - Frontend y Pruebas QA', 'SENA-TR-4', GradeLevel.LevelStage.TECNICO, 4),
    ]
    trimestres_dict = {}
    for name, code, stage, order in trimestres_def:
        g, _ = GradeLevel.objects.get_or_create(
            institution_type=inst_type,
            code=code,
            defaults={'name': name, 'level_stage': stage, 'order': order}
        )
        trimestres_dict[code] = g

    # Áreas de Formación y Competencias
    areas_sena = [
        ('Desarrollo de Software y Tecnologías de la Información', 1, [
            ('Análisis y Especificación de Requisitos de Software', 'SENA-REQ-01', 'Levantamiento de requerimientos y casos de uso.'),
            ('Desarrollo de Software Web y Móvil', 'SENA-DEV-01', 'Programación con arquitecturas modernas.'),
            ('Diseño y Administración de Bases de Datos', 'SENA-BD-01', 'Modelamiento relacional y SQL.'),
            ('Pruebas y Despliegue de Calidad (QA)', 'SENA-QA-01', 'Testing unitario, integración y CI/CD.')
        ]),
        ('Competencias Clave y Transversales SENA', 2, [
            ('Inglés Técnico para TI', 'SENA-ING-01', 'Lectura técnica y comunicación internacional.'),
            ('Seguridad y Salud en el Trabajo (SST)', 'SENA-SST-01', 'Normativa de prevención y autocuidado.'),
            ('Ética y Cultura de Paz', 'SENA-ETI-01', 'Habilidades para la vida y convivencia laboral.')
        ])
    ]
    for area_name, order, subjects in areas_sena:
        area, _ = KnowledgeArea.objects.get_or_create(
            institution_type=inst_type,
            name=area_name,
            defaults={'order': order}
        )
        for s_name, s_code, s_desc in subjects:
            subj, _ = Subject.objects.get_or_create(
                institution_type=inst_type,
                code=s_code,
                defaults={'name': s_name, 'area': area, 'description': s_desc}
            )
            # Vincular a Trimestre I y II
            for tr_code in ['SENA-TR-1', 'SENA-TR-2']:
                if tr_code in trimestres_dict:
                    GradeSubject.objects.get_or_create(
                        grade_level=trimestres_dict[tr_code],
                        subject=subj,
                        defaults={'weekly_hours': 6, 'weight_percentage': Decimal('100.00')}
                    )

    # Fichas (Cursos)
    fichas_def = [
        ('Ficha 2670123 - ADSO', 'SENA-TR-1', 'Ambiente 301 - Sistemas', 30),
        ('Ficha 2670124 - ADSO', 'SENA-TR-2', 'Ambiente 302 - Software', 30),
        ('Ficha 2580911 - Redes y Datos', 'SENA-TR-3', 'Laboratorio de Redes y Telecomunicaciones', 28),
    ]
    fichas_dict = {}
    for name, g_code, classroom, cap in fichas_def:
        if g_code in trimestres_dict:
            f, _ = CourseSection.objects.get_or_create(
                academic_year=year,
                grade_level=trimestres_dict[g_code],
                name=name,
                defaults={'classroom': classroom, 'capacity': cap, 'is_active': True}
            )
            fichas_dict[name] = f

    # Aprendices de Ejemplo para SENA
    aprendices_def = [
        ('987000101', 'Sebastián', 'Castro Ramos', 'TI', 'Ficha 2670123 - ADSO'),
        ('987000102', 'Valeria', 'Gómez Jaramillo', 'TI', 'Ficha 2670123 - ADSO'),
        ('987000103', 'Mateo', 'Ríos Quintana', 'CC', 'Ficha 2670124 - ADSO'),
        ('987000104', 'Camila', 'Hernández Paz', 'CC', 'Ficha 2670124 - ADSO'),
    ]
    for doc, first, last, dtype, f_name in aprendices_def:
        user, _ = CustomUser.objects.get_or_create(
            document_number=doc,
            defaults={
                'username': f'aprendiz_{doc}',
                'first_name': first,
                'last_name': last,
                'document_type': dtype,
                'role': CustomUser.Role.STUDENT,
                'email': f'{first.lower()}.{last.lower().split()[0]}@sena.edu.co'
            }
        )
        if not user.has_usable_password():
            user.set_password(doc)
            user.save()
        st_prof, _ = StudentProfile.objects.get_or_create(
            user=user,
            defaults={'student_code': f'AP-{doc[-4:]}', 'blood_type': 'O+'}
        )
        if f_name in fichas_dict:
            Enrollment.objects.get_or_create(
                student=st_prof,
                academic_year=year,
                course_section=fichas_dict[f_name],
                defaults={'status': Enrollment.Status.ACTIVE}
            )


def _provision_universidad(year):
    inst_type = InstitutionSetting.InstitutionType.UNIVERSIDAD
    # Semestres
    semestres_def = [
        ('Semestre I', 'UNI-SEM-1', GradeLevel.LevelStage.SUPERIOR, 1),
        ('Semestre II', 'UNI-SEM-2', GradeLevel.LevelStage.SUPERIOR, 2),
        ('Semestre III', 'UNI-SEM-3', GradeLevel.LevelStage.SUPERIOR, 3),
        ('Semestre IV', 'UNI-SEM-4', GradeLevel.LevelStage.SUPERIOR, 4),
        ('Semestre V', 'UNI-SEM-5', GradeLevel.LevelStage.SUPERIOR, 5),
    ]
    semestres_dict = {}
    for name, code, stage, order in semestres_def:
        g, _ = GradeLevel.objects.get_or_create(
            institution_type=inst_type,
            code=code,
            defaults={'name': name, 'level_stage': stage, 'order': order}
        )
        semestres_dict[code] = g

    # Áreas y Materias Universitarias
    areas_uni = [
        ('Facultad de Ingeniería y Ciencias Básicas', 1, [
            ('Cálculo Diferencial e Integral', 'UNI-CALC1', 'Límites, derivadas, integrales y aplicaciones.'),
            ('Álgebra Lineal y Geometría Analítica', 'UNI-ALG1', 'Matrices, vectores y transformaciones lineales.'),
            ('Física Mecánica y Ondas', 'UNI-FIS1', 'Leyes de movimiento, trabajo y energía.')
        ]),
        ('Ingeniería de Software y Sistemas', 2, [
            ('Algoritmos y Estructuras de Datos', 'UNI-EDD1', 'Estructuras dinámicas, grafos y complejidad.'),
            ('Bases de Datos Relacionales y NoSQL', 'UNI-BDA1', 'Diseño relacional, ACID y MongoDB.'),
            ('Arquitectura de Sistemas Distribuidos', 'UNI-ARQ1', 'Microservicios, patrones y cloud computing.')
        ]),
        ('Humanidades y Metodología', 3, [
            ('Metodología de la Investigación Científica', 'UNI-INV1', 'Rigor científico y redacción de papers.'),
            ('Ética Profesional y Ciudadana', 'UNI-ETI1', 'Deontología y dilemas éticos en ingeniería.')
        ])
    ]
    for area_name, order, subjects in areas_uni:
        area, _ = KnowledgeArea.objects.get_or_create(
            institution_type=inst_type,
            name=area_name,
            defaults={'order': order}
        )
        for s_name, s_code, s_desc in subjects:
            subj, _ = Subject.objects.get_or_create(
                institution_type=inst_type,
                code=s_code,
                defaults={'name': s_name, 'area': area, 'description': s_desc}
            )
            for sem_code in ['UNI-SEM-1', 'UNI-SEM-2']:
                if sem_code in semestres_dict:
                    GradeSubject.objects.get_or_create(
                        grade_level=semestres_dict[sem_code],
                        subject=subj,
                        defaults={'weekly_hours': 4, 'weight_percentage': Decimal('100.00')}
                    )

    # Grupos Universitarios
    grupos_def = [
        ('Grupo 101 - Ingeniería', 'UNI-SEM-1', 'Edificio B - Aula 204', 35),
        ('Grupo 102 - Administración', 'UNI-SEM-1', 'Edificio A - Aula 105', 35),
        ('Grupo 201 - Ingeniería', 'UNI-SEM-2', 'Edificio B - Aula 301', 32),
    ]
    grupos_dict = {}
    for name, g_code, classroom, cap in grupos_def:
        if g_code in semestres_dict:
            grp, _ = CourseSection.objects.get_or_create(
                academic_year=year,
                grade_level=semestres_dict[g_code],
                name=name,
                defaults={'classroom': classroom, 'capacity': cap, 'is_active': True}
            )
            grupos_dict[name] = grp

    # Estudiantes Universitarios de Ejemplo
    alumnos_uni = [
        ('10200001', 'Daniel', 'Ospina Restrepo', 'CC', 'Grupo 101 - Ingeniería'),
        ('10200002', 'Juliana', 'Duque Londoño', 'CC', 'Grupo 101 - Ingeniería'),
        ('10200003', 'Andrés Felipe', 'Torres Benítez', 'CC', 'Grupo 201 - Ingeniería'),
    ]
    for doc, first, last, dtype, g_name in alumnos_uni:
        user, _ = CustomUser.objects.get_or_create(
            document_number=doc,
            defaults={
                'username': f'univ_{doc}',
                'first_name': first,
                'last_name': last,
                'document_type': dtype,
                'role': CustomUser.Role.STUDENT,
                'email': f'{first.lower().replace(" ", "")}.{last.lower().split()[0]}@universidad.edu.co'
            }
        )
        if not user.has_usable_password():
            user.set_password(doc)
            user.save()
        st_prof, _ = StudentProfile.objects.get_or_create(
            user=user,
            defaults={'student_code': f'ESTU-{doc[-4:]}', 'blood_type': 'A+'}
        )
        if g_name in grupos_dict:
            Enrollment.objects.get_or_create(
                student=st_prof,
                academic_year=year,
                course_section=grupos_dict[g_name],
                defaults={'status': Enrollment.Status.ACTIVE}
            )


def _provision_academia(year):
    inst_type = InstitutionSetting.InstitutionType.ACADEMIA
    # Niveles
    niveles_def = [
        ('Nivel Principiante (A1)', 'ACAD-A1', GradeLevel.LevelStage.CONTINUA, 1),
        ('Nivel Elemental (A2)', 'ACAD-A2', GradeLevel.LevelStage.CONTINUA, 2),
        ('Nivel Intermedio (B1)', 'ACAD-B1', GradeLevel.LevelStage.CONTINUA, 3),
        ('Nivel Intermedio Alto (B2)', 'ACAD-B2', GradeLevel.LevelStage.CONTINUA, 4),
    ]
    niveles_dict = {}
    for name, code, stage, order in niveles_def:
        g, _ = GradeLevel.objects.get_or_create(
            institution_type=inst_type,
            code=code,
            defaults={'name': name, 'level_stage': stage, 'order': order}
        )
        niveles_dict[code] = g

    # Áreas y Módulos / Talleres
    areas_acad = [
        ('Programa de Inglés Comunicativo', 1, [
            ('Grammar, Vocabulary & Structures', 'ACAD-GRM1', 'Estructuras gramaticales y vocabulario base.'),
            ('Conversation Club & Fluency Workshop', 'ACAD-CONV1', 'Inmersión oral, debates y pronunciación.'),
            ('Business English & Corporate Communication', 'ACAD-BUS1', 'Inglés de negocios y presentaciones.')
        ]),
        ('Talleres Prácticos y Habilidades', 2, [
            ('Taller de Fonética y Reducción de Acento', 'ACAD-FON1', 'Fonemas, entonación y acentuación en inglés.'),
            ('Taller de Redacción y Escritura Creativa', 'ACAD-WRT1', 'Ensayos, correos y artículos.')
        ])
    ]
    for area_name, order, subjects in areas_acad:
        area, _ = KnowledgeArea.objects.get_or_create(
            institution_type=inst_type,
            name=area_name,
            defaults={'order': order}
        )
        for s_name, s_code, s_desc in subjects:
            subj, _ = Subject.objects.get_or_create(
                institution_type=inst_type,
                code=s_code,
                defaults={'name': s_name, 'area': area, 'description': s_desc}
            )
            for n_code in ['ACAD-A1', 'ACAD-B1']:
                if n_code in niveles_dict:
                    GradeSubject.objects.get_or_create(
                        grade_level=niveles_dict[n_code],
                        subject=subj,
                        defaults={'weekly_hours': 3, 'weight_percentage': Decimal('100.00')}
                    )

    # Clases / Grupos de Academia
    clases_def = [
        ('Clase A1 - Horario Mañana', 'ACAD-A1', 'Salón Virtual Alpha', 20),
        ('Clase B1 - Horario Noche', 'ACAD-B1', 'Salón Virtual Beta', 20),
        ('Diplomado B2 - Sábados Intensivo', 'ACAD-B1', 'Sede Central - Auditorio 1', 25),
    ]
    clases_dict = {}
    for name, g_code, classroom, cap in clases_def:
        if g_code in niveles_dict:
            cls_sec, _ = CourseSection.objects.get_or_create(
                academic_year=year,
                grade_level=niveles_dict[g_code],
                name=name,
                defaults={'classroom': classroom, 'capacity': cap, 'is_active': True}
            )
            clases_dict[name] = cls_sec

    # Alumnos de Academia de Ejemplo
    alumnos_acad = [
        ('10300001', 'Natalia', 'Vargas Salazar', 'CC', 'Clase A1 - Horario Mañana'),
        ('10300002', 'Felipe', 'Jaramillo Osorio', 'CC', 'Clase A1 - Horario Mañana'),
        ('10300003', 'Carolina', 'Rivas Montoya', 'CC', 'Clase B1 - Horario Noche'),
    ]
    for doc, first, last, dtype, c_name in alumnos_acad:
        user, _ = CustomUser.objects.get_or_create(
            document_number=doc,
            defaults={
                'username': f'acad_{doc}',
                'first_name': first,
                'last_name': last,
                'document_type': dtype,
                'role': CustomUser.Role.STUDENT,
                'email': f'{first.lower()}.{last.lower()}@academia.edu.co'
            }
        )
        if not user.has_usable_password():
            user.set_password(doc)
            user.save()
        st_prof, _ = StudentProfile.objects.get_or_create(
            user=user,
            defaults={'student_code': f'ALUM-{doc[-4:]}', 'blood_type': 'B+'}
        )
        if c_name in clases_dict:
            Enrollment.objects.get_or_create(
                student=st_prof,
                academic_year=year,
                course_section=clases_dict[c_name],
                defaults={'status': Enrollment.Status.ACTIVE}
            )
