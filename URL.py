from django.urls import path
from . import views

urlpatterns = [
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-users/', views.manage_users, name='manage_users'),
    path('export-stock-report-csv/', views.export_stock_report_csv, name='export_stock_report_csv'),
]