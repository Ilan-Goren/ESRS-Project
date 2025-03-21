from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'supplier'

urlpatterns = [
    # Authentication
    path('login/', views.supplier_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Dashboard
    path('dashboard/', views.supplier_dashboard, name='dashboard'),
    
    # Orders
    path('orders/', views.orders_list, name='orders_list'),
    path('orders/detail/<int:pk>/', views.order_detail, name='order_detail'),
    path('orders/update-status/<int:pk>/', views.order_update_status, name='update_status'),
    
    # History
    path('orders/history/', views.orders_history, name='orders_history'),
    
    # Profile
    path('profile/', views.supplier_profile, name='profile'),
    path('profile/edit/', views.supplier_profile_edit, name='profile_edit'),
]