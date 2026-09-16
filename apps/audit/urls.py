from django.urls import path
from . import views

app_name = 'audit'

urlpatterns = [
    path('', views.audit_list_view, name='list'),
    path('export/csv/', views.export_audit_csv_view, name='export_csv'),
    path('<int:log_id>/detail/', views.audit_detail_modal_view, name='detail'),
]
