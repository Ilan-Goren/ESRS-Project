"""
URL patterns for the supplier application.
"""

from django.urls import path

from . import views

app_name = 'supplier'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.supplier_dashboard, name='dashboard'),
    
    # Order Management
    path('orders/', views.view_orders, name='view_orders'),
    path('orders/<int:order_id>/', views.order_details, name='order_details'),
    path('orders/<int:order_id>/update/', views.update_delivery_status, name='update_delivery_status'),
    
    # Past Orders
    path('past-orders/', views.past_orders, name='past_orders'),
    
    # Profile Management
    path('profile/', views.supplier_profile, name='supplier_profile'),
    
    # Performance Metrics
    path('performance/', views.performance_metrics, name='performance_metrics'),
]