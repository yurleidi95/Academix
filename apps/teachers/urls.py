from django.urls import path
from . import views

app_name = 'teachers'

urlpatterns = [
    path('', views.teachers_list_view, name='list'),
    path('assign/', views.assign_teacher_view, name='assign'),
    path('create/', views.create_teacher_view, name='create'),
]

