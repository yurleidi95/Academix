from django.urls import path
from . import views

app_name = 'homework'

urlpatterns = [
    path('', views.homework_index_view, name='index'),
    path('create/', views.create_homework_view, name='create'),
    path('<int:homework_id>/submit/', views.submit_homework_view, name='submit'),
    path('submission/<int:submission_id>/grade/', views.grade_submission_view, name='grade'),
]
