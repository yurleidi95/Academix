from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    path('', views.students_list_view, name='list'),
    path('enroll/', views.enroll_student_view, name='enroll'),
    path('create/', views.create_student_view, name='create'),
]

