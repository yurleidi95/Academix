from apps.courses.models import InstitutionSetting

def institution_context(request):
    """
    Inyecta la configuración institucional global y su terminología adaptable en todas las plantillas.
    Permite usar {{ institution.term_student }}, {{ institution.term_teacher }}, etc.
    """
    try:
        settings = InstitutionSetting.get_settings()
    except Exception:
        settings = None

    return {
        'institution': settings,
    }
