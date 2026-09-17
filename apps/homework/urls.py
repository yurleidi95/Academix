from django.urls import path
from . import views

app_name = 'homework'

urlpatterns = [
    path('', views.homework_index_view, name='index'),
    path('course/<int:section_id>/', views.homework_course_matrix_view, name='course_matrix'),
    path('course/<int:section_id>/bulk-grade/', views.bulk_grade_course_view, name='bulk_grade'),
    path('grade-cell/', views.manual_grade_cell_view, name='grade_cell'),
    path('create/', views.create_homework_view, name='create'),
    path('<int:homework_id>/submit/', views.submit_homework_view, name='submit'),
    path('submission/<int:submission_id>/grade/', views.grade_submission_view, name='grade'),
]
