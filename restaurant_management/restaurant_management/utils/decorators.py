"""
Utility decorators for the restaurant management system.

This module contains decorators used throughout the application to handle
common patterns like permission checks and request validation.
"""

from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from django.urls import reverse
from django.utils.translation import gettext as _

from restaurant_management.utils.constants import (
    ADMIN_ROLE, MANAGER_ROLE, STAFF_ROLE, SUPPLIER_ROLE
)


def ajax_required(view_func):
    """
    Decorator to ensure a view can only be accessed via AJAX requests.
    
    Args:
        view_func: The view function to decorate.
        
    Returns:
        function: The decorated view function.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'error': 'This endpoint only accepts AJAX requests'}, status=400)
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def check_user_role(user, roles):
    """
    Check if a user has one of the specified roles.
    
    Args:
        user: The user to check.
        roles: A list of role names or a single role name.
        
    Returns:
        bool: True if the user has one of the specified roles, False otherwise.
    """
    if not hasattr(user, 'profile'):
        return False
    
    if isinstance(roles, str):
        return user.profile.role == roles
    else:
        return user.profile.role in roles


def role_required(roles):
    """
    Decorator to restrict view access to users with specific roles.
    
    Args:
        roles: A list of role names or a single role name.
        
    Returns:
        function: Decorator function.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not check_user_role(request.user, roles):
                messages.error(request, _("You don't have permission to access this page."))
                return redirect('landing_page')
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def supplier_user_required(view_func):
    """
    Decorator to restrict view access to supplier users only.
    
    Args:
        view_func: The view function to decorate.
        
    Returns:
        function: The decorated view function.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not check_user_role(request.user, SUPPLIER_ROLE):
            messages.error(request, _("This area is restricted to supplier users."))
            return redirect('landing_page')
        
        # Check if the user has a supplier profile
        if not hasattr(request.user, 'supplier_profile'):
            messages.error(request, _("Your supplier profile is not properly set up."))
            return redirect('landing_page')
        
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def store_user_required(view_func):
    """
    Decorator to restrict view access to store users (admin, manager, staff) only.
    
    Args:
        view_func: The view function to decorate.
        
    Returns:
        function: The decorated view function.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        if not check_user_role(request.user, [ADMIN_ROLE, MANAGER_ROLE, STAFF_ROLE]):
            messages.error(request, _("This area is restricted to store staff."))
            return redirect('landing_page')
        return view_func(request, *args, **kwargs)
    return _wrapped_view


def admin_required(view_func):
    """
    Decorator to restrict view access to admin users only.
    
    Args:
        view_func: The view function to decorate.
        
    Returns:
        function: The decorated view function.
    """
    return role_required(ADMIN_ROLE)(view_func)


def manager_or_admin_required(view_func):
    """
    Decorator to restrict view access to manager or admin users only.
    
    Args:
        view_func: The view function to decorate.
        
    Returns:
        function: The decorated view function.
    """
    return role_required([ADMIN_ROLE, MANAGER_ROLE])(view_func)