"""
URL patterns for the store application.
"""

from django.urls import path
from django.contrib.auth import views as auth_views

from . import views
from .views import InventoryListCreateAPIView, InventoryRetrieveUpdateDestroyAPIView, dashboard_api_view
from .forms import CustomAuthenticationForm

app_name = 'store'

urlpatterns = [
    # Dashboards
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    
    # Inventory Management
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/add/', views.add_inventory, name='add_inventory'),
    path('inventory/edit/<int:pk>/', views.edit_inventory, name='edit_inventory'),
    path('inventory/transaction/', views.inventory_transaction, name='inventory_transaction'),
    path('inventory/low-stock/', views.low_stock_alerts, name='low_stock_alerts'),
    path('inventory/expiry-dates/', views.expiry_dates, name='expiry_dates'),
    
    # Order Management
    path('orders/', views.order_list, name='order_list'),
    path('orders/create/', views.create_order, name='create_order'),
    path('orders/<int:order_id>/add-items/', views.add_order_items, name='add_order_items'),
    path('orders/<int:order_id>/update-status/', views.update_order_status, name='update_order_status'),
    path('orders/<int:order_id>/details/', views.order_details, name='order_details'),
    
    # User Management
    path('users/', views.manage_users, name='manage_users'),
    path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
    
    # Reports
    path('reports/stock/', views.stock_report, name='stock_report'),
    path('reports/orders/', views.order_summary, name='order_summary'),
    path('reports/suppliers/', views.supplier_performance, name='supplier_performance'),
    
    # Settings
    path('settings/', views.configure_settings, name='configure_settings'),
    
    # Supplier Management
    path('suppliers/', views.manage_suppliers, name='manage_suppliers'),
    
    # API Endpoints
    path('api/inventory/', views.InventoryListCreateAPIView.as_view(), name='inventory_api_list_create'),
    path('api/inventory/<int:pk>/', views.InventoryRetrieveUpdateDestroyAPIView.as_view(), name='inventory_api_detail'),
    path('api/dashboard/', views.dashboard_api_view, name='dashboard_api'),
    
    # Add these new dashboard API endpoints
    path('api/dashboard/manager/', views.manager_dashboard_api_view, name='manager_dashboard_api'),
    path('api/dashboard/staff/', views.staff_dashboard_api_view, name='staff_dashboard_api'),
    path('api/dashboard/supplier/', views.supplier_dashboard_api_view, name='supplier_dashboard_api'),
]