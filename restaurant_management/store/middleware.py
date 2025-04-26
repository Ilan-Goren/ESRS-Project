"""
Middleware for the store application.

This module contains middleware classes used to process requests and responses
for the store application.
"""

import datetime
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse, resolve
from django.http import HttpResponseRedirect

from restaurant_management.utils.constants import SUPPLIER_ROLE
from .models import Inventory


class RoleRestrictedMiddleware:
    """
    Middleware to ensure users can only access routes appropriate for their role.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Process the request
        if request.user.is_authenticated:
            try:
                # Check if the user has a profile
                profile = request.user.profile
                
                # Get the current URL name
                resolver_match = resolve(request.path_info)
                url_name = resolver_match.url_name
                
                # Restrict supplier users from accessing store routes
                if profile.role == SUPPLIER_ROLE and request.path.startswith('/store/'):
                    messages.error(request, "Supplier users cannot access store management functions.")
                    return HttpResponseRedirect(reverse('supplier:dashboard'))
                
                # Add the user's role to the request for easy access in views
                request.user_role = profile.role
                
            except Exception:
                # If there's any error (e.g., user doesn't have a profile),
                # continue with the request and let the view handle it
                pass
        
        # Process the response
        response = self.get_response(request)
        return response


class ExpiryDateCheckMiddleware:
    """
    Middleware to check for expiring inventory items and notify staff.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Keep track of when we last checked for expiring items
        self.last_check = None
    
    def __call__(self, request):
        # Only check once per day and only for authenticated non-supplier users
        if (
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and 
            request.user.profile.role != SUPPLIER_ROLE and
            (self.last_check is None or timezone.now() - self.last_check > datetime.timedelta(days=1))
        ):
            # Update the last check time
            self.last_check = timezone.now()
            
            # Check for items that will expire in the next 7 days
            today = timezone.now().date()
            expiry_threshold = today + datetime.timedelta(days=7)
            
            expiring_soon = Inventory.objects.filter(
                expiry_date__isnull=False,
                expiry_date__gt=today,
                expiry_date__lte=expiry_threshold
            ).count()
            
            expired = Inventory.objects.filter(
                expiry_date__isnull=False,
                expiry_date__lt=today
            ).count()
            
            # Only add messages if there are items to report
            if expiring_soon > 0:
                messages.warning(
                    request,
                    f"{expiring_soon} inventory items will expire within the next 7 days. "
                    f"<a href='{reverse('store:expiry_dates')}'>View expiring items</a>"
                )
            
            if expired > 0:
                messages.error(
                    request,
                    f"{expired} inventory items have expired. "
                    f"<a href='{reverse('store:expiry_dates')}'>View expired items</a>"
                )
        
        # Process the response
        response = self.get_response(request)
        return response


class LowStockAlertMiddleware:
    """
    Middleware to check for low stock items and notify staff.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Keep track of when we last checked for low stock items
        self.last_check = None
    
    def __call__(self, request):
        # Only check once per day and only for authenticated non-supplier users
        if (
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and 
            request.user.profile.role != SUPPLIER_ROLE and
            (self.last_check is None or timezone.now() - self.last_check > datetime.timedelta(days=1))
        ):
            # Update the last check time
            self.last_check = timezone.now()
            
            # Check for items that are at or below their reorder level
            from .models import Inventory
            from django.db.models import F
            
            low_stock = Inventory.objects.filter(
                quantity__lte=F('reorder_level')
            ).count()
            
            # Only add message if there are items to report
            if low_stock > 0:
                messages.warning(
                    request,
                    f"{low_stock} inventory items are at or below their reorder level. "
                    f"<a href='{reverse('store:low_stock_alerts')}'>View low stock items</a>"
                )
        
        # Process the response
        response = self.get_response(request)
        return response