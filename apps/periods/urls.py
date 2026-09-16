from django.urls import path
from . import views

app_name = 'periods'

urlpatterns = [
    path('', views.periods_list_view, name='list'),
    path('<int:period_id>/status/', views.update_status_htmx, name='update_status'),
]
