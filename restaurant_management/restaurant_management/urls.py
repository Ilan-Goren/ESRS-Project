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
            
            if not username or not password:
                return JsonResponse({'message': 'Username/email and password required'}, status=400)
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                login(request, user)
                try:
                    user_role = user.userprofile.role
                except AttributeError:
                    if user.is_superuser:
                        user_role = 'admin'
                    else:
                        user_role = 'unknown'
                
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
]