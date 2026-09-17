from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.students_list_view, name='list'),
    path('enroll/', views.enroll_student_view, name='enroll'),
    path('create/', views.create_student_view, name='create'),
    path('<int:student_id>/observations/', views.student_observations_view, name='observations'),
    path('<int:student_id>/observations/create/', views.create_observation_view, name='create_observation'),
    path('bulk-upload/', views.bulk_upload_students_view, name='bulk_upload'),
    path('download-template/', views.download_student_template_csv, name='download_template'),
    path('enrollment/<int:enrollment_id>/confirm/', views.confirm_enrollment_view, name='confirm_enrollment'),
    path('enrollment/<int:enrollment_id>/cancel/', views.cancel_enrollment_view, name='cancel_enrollment'),
]


