from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'store'

urlpatterns = [
    # Authentication
    path('login/', views.store_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('redirect-to-dashboard/', views.redirect_to_dashboard, name='redirect_to_dashboard'),
    
    # Dashboards
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manager-dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('staff-dashboard/', views.staff_dashboard, name='staff_dashboard'),
    
    # Inventory Management
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/add/', views.inventory_add, name='inventory_add'),
    path('inventory/edit/<int:pk>/', views.inventory_edit, name='inventory_edit'),
    path('inventory/delete/<int:pk>/', views.inventory_delete, name='inventory_delete'),
    path('inventory/low-stock/', views.inventory_low_stock, name='inventory_low_stock'),
    path('inventory/expiring/', views.inventory_expiring, name='inventory_expiring'),
    
    # Order Management
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/add/', views.order_add, name='order_add'),
    path('orders/detail/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/edit/<int:pk>/', views.order_edit, name='order_edit'),
    path('orders/delete/<int:pk>/', views.order_delete, name='order_delete'),
    path('orders/approve/<int:pk>/', views.order_approve, name='order_approve'),
    
    # Transaction Management
    path('transactions/', views.transactions_list, name='transactions_list'),
    path('transactions/add/', views.transaction_add, name='transaction_add'),
    
    # User Management
    path('users/', views.users_list, name='users_list'),
    path('users/add/', views.user_add, name='user_add'),
    path('users/edit/<int:pk>/', views.user_edit, name='user_edit'),
    path('users/delete/<int:pk>/', views.user_delete, name='user_delete'),
    
    # Supplier Management
    path('suppliers/', views.suppliers_list, name='suppliers_list'),
    path('suppliers/add/', views.supplier_add, name='supplier_add'),
    path('suppliers/edit/<int:pk>/', views.supplier_edit, name='supplier_edit'),
    path('suppliers/delete/<int:pk>/', views.supplier_delete, name='supplier_delete'),
    path('suppliers/performance/<int:pk>/', views.supplier_performance, name='supplier_performance'),
    
    # Reports
    path('reports/stock/', views.report_stock, name='report_stock'),
    path('reports/orders/', views.report_orders, name='report_orders'),
    path('reports/suppliers/', views.report_suppliers, name='report_suppliers'),
    path('reports/export/<str:report_type>/', views.report_export, name='report_export'),
]