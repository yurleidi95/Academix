from django.urls import path
from . import views

app_name = 'rules'

urlpatterns = [
    path('closing/', views.closing_manager_view, name='closing_manager'),
    path('period/<int:period_id>/close/', views.close_period_view, name='close_period'),
    path('period/<int:period_id>/reopen/', views.reopen_period_view, name='reopen_period'),
    path('year/<int:year_id>/close-annual/', views.execute_year_closing_view, name='execute_year_closing'),
]
