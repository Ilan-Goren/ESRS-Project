"""
Custom authentication backends for the restaurant management system.

These backends extend Django's default authentication to support
user roles and specialized login flows.
"""

from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User
from django.db.models import Q

from .models import UserProfile


class CustomUserBackend(ModelBackend):
    """
    Custom authentication backend that allows users to login with
    either username or email and validates user role permissions.
    """
    
    def authenticate(self, request, username=None, password=None, **kwargs):
        """
        Authenticate a user based on username/email and password.
        
        Args:
            request: The current request.
            username: The username or email provided for authentication.
            password: The password provided for authentication.
        
        Returns:
            User: The authenticated user if successful, None otherwise.
        """
        if username is None or password is None:
            return None
        
        # Try to find a user that matches either username or email
        try:
            user = User.objects.get(Q(username=username) | Q(email=username))
        except User.DoesNotExist:
            # Run the default password hasher to prevent timing attacks
            User().set_password(password)
            return None
        
        # Check password
        if user.check_password(password):
            # Check if user has the required profile for the current app
            app_name = request.path.split('/')[1] if request.path else ''
            
            try:
                profile = user.profile
                
                # If trying to access supplier functionality, ensure user has supplier role
                if app_name == 'supplier' and profile.role != 'supplier':
                    return None
                
                # If trying to access store functionality, ensure user is not a supplier
                if app_name == 'store' and profile.role == 'supplier':
                    return None
                
            except UserProfile.DoesNotExist:
                # User doesn't have a profile, which is required for our system
                return None
            
            return user
        
        return None