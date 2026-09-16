from django.urls import path
from . import views

app_name = 'attendance'

urlpatterns = [
    path('', views.attendance_index_view, name='index'),
    path('sheet/', views.attendance_sheet_view, name='sheet'),
    path('record/<int:record_id>/update/', views.update_record_inline_view, name='update_record'),
    path('session/<int:session_id>/mark-all-present/', views.mark_all_present_view, name='mark_all_present'),
]
