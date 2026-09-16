from django.urls import path
from . import views

app_name = 'courses'

urlpatterns = [
    path('academic-structure/', views.academic_structure_view, name='academic_structure'),
    path('sections/partial/', views.sections_partial, name='sections_partial'),
    path('sections/create/', views.create_section_view, name='create_section'),
]
