"""
URL configuration for restaurant_management project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include  # Make sure 'path' is imported here
from django.contrib.auth import views as auth_views

from store.views import landing_page, register_user
from store.views import dashboard_api_view
from store.views import InventoryListCreateAPIView
from store.views import UserListView
from store.forms import CustomAuthenticationForm

from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.views import View
from django.views.decorators.csrf import csrf_exempt
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
            role = data.get('role')
            
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
    path('api/auth/login/', csrf_exempt(APILoginView.as_view()), name='api_login'),
    path('api/dashboard/', dashboard_api_view),
    path('api/inventory/', InventoryListCreateAPIView.as_view()),
    path('api/users/', UserListView.as_view()),
]