from django.urls import path
from . import views

app_name = 'subjects'

urlpatterns = [
    path('curriculum/', views.curriculum_view, name='curriculum'),
    path('by-grade/partial/', views.subjects_by_grade_partial, name='by_grade_partial'),
]
