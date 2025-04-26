"""
Custom decorators for the store application.

These decorators help manage role-based access control for various views.
"""

from django.shortcuts import redirect
from django.contrib import messages
from django.http import HttpResponseForbidden
from functools import wraps

from .models import UserProfile


def role_required(roles):
    """
    Decorator to check if the user has the required role(s).
    
    Args:
        roles (str or list): Required role(s) to access the view.
            Can be a single role string or a list of acceptable roles.
    
    Returns:
        function: Decorated view function that checks user roles.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            try:
                profile = request.user.profile
            except UserProfile.DoesNotExist:
                messages.error(request, "You need a profile to access this page.")
                return redirect('landing_page')
            
            # Convert single role to list for consistent handling
            if isinstance(roles, str):
                required_roles = [roles]
            else:
                required_roles = roles
            
            # Check if user has any of the required roles
            if profile.role not in required_roles:
                messages.error(request, "You don't have permission to access this page.")
                return redirect('landing_page')
            
            return view_func(request, *args, **kwargs)
        
        return _wrapped_view
    
    return decorator


def admin_required(view_func):
    """
    Decorator specifically for admin-only views.
    
    Returns:
        function: Decorated view function that checks for admin role.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            profile = request.user.profile
            if not profile.is_admin:
                messages.error(request, "Admin privileges required.")
                return redirect('landing_page')
        except UserProfile.DoesNotExist:
            messages.error(request, "You need an admin profile to access this page.")
            return redirect('landing_page')
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view


def manager_required(view_func):
    """
    Decorator specifically for manager-only views.
    
    Returns:
        function: Decorated view function that checks for manager role.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            profile = request.user.profile
            if not profile.is_manager:
                messages.error(request, "Manager privileges required.")
                return redirect('landing_page')
        except UserProfile.DoesNotExist:
            messages.error(request, "You need a manager profile to access this page.")
            return redirect('landing_page')
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view


def staff_required(view_func):
    """
    Decorator specifically for staff-only views.
    
    Returns:
        function: Decorated view function that checks for staff role.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            profile = request.user.profile
            if not profile.is_staff:
                messages.error(request, "Staff privileges required.")
                return redirect('landing_page')
        except UserProfile.DoesNotExist:
            messages.error(request, "You need a staff profile to access this page.")
            return redirect('landing_page')
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view