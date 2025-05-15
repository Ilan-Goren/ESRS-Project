"""
URL configuration for restaurant_management project.
"""

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

from store.views import (
    landing_page, register_user, dashboard_api_view,
    InventoryListCreateAPIView, UserListView, api_register_view,
    user_detail_api_view
)

from store.views import (
    supplier_dashboard_api_view,
    orders_api_view,
    supplier_orders_api_view,
    update_order_status, 

    manager_dashboard_api_view,
    suppliers_api_view,
    supplier_detail_api_view,

    staff_dashboard_api_view,
    test_dashboard_view
)

from store.forms import CustomAuthenticationForm

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.views import View
from django.http import JsonResponse
import json
from django.conf import settings
import jwt
from datetime import datetime, timedelta
import uuid

from rest_framework_simplejwt.tokens import RefreshToken

class APILoginView(View):
    def post(self, request):
        try:
            body_unicode = request.body.decode('utf-8')
            data = json.loads(body_unicode)
            username = data.get('username') or data.get('email')
            password = data.get('password')
            selected_role = data.get('role')  # Get the role the user selected in the UI
            
            print(f"Login attempt - Username: {username}, Selected role: {selected_role}")
            
            if not username or not password:
                return JsonResponse({'message': 'Username/email and password required'}, status=400)
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                
                # Get role from users table directly using raw SQL
                from django.db import connection
                user_role = None
                
                try:
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "SELECT role FROM users WHERE id = %s OR email = %s",
                            [user.id, user.email]
                        )
                        result = cursor.fetchone()
                        if result:
                            user_role = result[0]
                            print(f"Found role in users table: {user_role}")
                except Exception as e:
                    print(f"Error querying users table: {str(e)}")
                
                # Fallback if no role found in users table
                if not user_role:
                    # Allow the selected role if user is a superuser
                    if user.is_superuser and selected_role:
                        user_role = selected_role
                        print(f"Using selected role for superuser: {user_role}")
                    else:
                        # Default roles based on Django permissions
                        if user.is_superuser:
                            user_role = 'admin'
                        elif user.is_staff:
                            user_role = 'staff'
                        else:
                            # If we got here, just use the selected role as a last resort
                            user_role = selected_role or 'staff'
                        print(f"Using fallback role: {user_role}")
                
                # Ensure the role is one of the valid options
                valid_roles = ['admin', 'manager', 'staff', 'supplier']
                if user_role not in valid_roles:
                    user_role = 'staff'  # Default to staff if invalid role
                
                # Generate standard JWT tokens
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                
                # Prepare user data
                user_data = {
                    'id': user.id,
                    'name': user.get_full_name() or user.username,
                    'username': user.username,
                    'email': user.email,
                    'is_superuser': user.is_superuser,
                    'role': user_role
                }
                
                print(f"Login successful - User: {user.username}, Role: {user_role}")
                
                return JsonResponse({
                    'message': 'Login successful',
                    'token': access_token,
                    'access': access_token,
                    'refresh': str(refresh),
                    'role': user_role,
                    'user': user_data
                })
            else:
                return JsonResponse({'message': 'Invalid credentials'}, status=401)
        except json.JSONDecodeError:
            return JsonResponse({'message': 'Invalid JSON payload'}, status=400)
        except Exception as e:
            print(f"Login error: {str(e)}")
            return JsonResponse({'message': 'Error during login', 'error': str(e)}, status=400)
urlpatterns = [
    # Django Admin
    path('admin/', admin.site.urls),
    
    # Authentication
    path('login/', auth_views.LoginView.as_view(
        template_name='registration/login.html',
        authentication_form=CustomAuthenticationForm
    ), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('register/', register_user, name='register'),
    
    # Landing Page
    path('', landing_page, name='landing_page'),
    
    # App URLs
    path('store/', include('store.urls')),
    path('supplier/', include('supplier.urls')),
    
    # API Endpoints
    path('api/auth/login/', csrf_exempt(APILoginView.as_view()), name='api_login'),
    path('api/auth/register/', api_register_view, name='api_register'),  # New registration endpoint
    path('api/dashboard/', dashboard_api_view),
    path('api/inventory/', InventoryListCreateAPIView.as_view()),
    path('api/users/', UserListView.as_view()),
    path('api/users/<int:user_id>/', user_detail_api_view, name='user_detail_api'),

    path('api/dashboard/supplier/', supplier_dashboard_api_view, name='supplier_dashboard_api'),
    path('api/orders/', orders_api_view, name='orders_api'),
    path('api/orders/supplier/', supplier_orders_api_view, name='supplier_orders_api'),
    path('api/orders/<int:order_id>/status/', update_order_status, name='update_order_status'),

    path('api/dashboard/manager/', manager_dashboard_api_view, name='manager_dashboard_api'),
    path('api/suppliers/', suppliers_api_view, name='suppliers_api'),
    path('api/suppliers/<int:supplier_id>/', supplier_detail_api_view, name='supplier_detail_api'),

    path('api/dashboard/staff/', staff_dashboard_api_view, name='staff_dashboard_api'),
    path('api/test-dashboard/', test_dashboard_view, name='test_dashboard'),

]