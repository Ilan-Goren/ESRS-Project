"""
Middleware for the supplier application.

This module contains middleware classes used to process requests and responses
for the supplier application.
"""

import datetime
from django.utils import timezone
from django.contrib import messages
from django.urls import reverse, resolve
from django.http import HttpResponseRedirect

from restaurant_management.utils.constants import SUPPLIER_ROLE
from .models import SupplierProfile
from store.models import Order


class SupplierAccessMiddleware:
    """
    Middleware to ensure only supplier users can access supplier routes.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        # Process the request
        if request.user.is_authenticated and request.path.startswith('/supplier/'):
            try:
                # Check if the user has a profile and is a supplier
                profile = request.user.profile
                
                if profile.role != SUPPLIER_ROLE:
                    messages.error(request, "Only supplier users can access the supplier portal.")
                    return HttpResponseRedirect(reverse('landing_page'))
                
                # Check if the user has a supplier profile
                try:
                    supplier_profile = request.user.supplier_profile
                except SupplierProfile.DoesNotExist:
                    messages.error(request, "Your supplier profile is not properly set up.")
                    return HttpResponseRedirect(reverse('landing_page'))
                
                # Add the supplier to the request for easy access in views
                request.supplier = supplier_profile.supplier
                
            except Exception:
                # If there's any error (e.g., user doesn't have a profile),
                # redirect to the landing page
                messages.error(request, "Access denied. Please log in as a supplier.")
                return HttpResponseRedirect(reverse('landing_page'))
        
        # Process the response
        response = self.get_response(request)
        return response


class PendingOrderAlertMiddleware:
    """
    Middleware to check for pending orders and notify suppliers.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Keep track of when we last checked for pending orders
        self.last_check = {}  # Dict to track per supplier
    
    def __call__(self, request):
        # Only check for authenticated supplier users
        if (
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and 
            request.user.profile.role == SUPPLIER_ROLE and
            hasattr(request.user, 'supplier_profile')
        ):
            supplier = request.user.supplier_profile.supplier
            supplier_id = supplier.id
            
            # Check if we need to check for this supplier
            if (
                supplier_id not in self.last_check or 
                timezone.now() - self.last_check[supplier_id] > datetime.timedelta(hours=6)
            ):
                # Update the last check time
                self.last_check[supplier_id] = timezone.now()
                
                # Check for pending orders
                pending_count = Order.objects.filter(
                    supplier=supplier,
                    status='pending'
                ).count()
                
                # Only add message if there are pending orders
                if pending_count > 0:
                    messages.info(
                        request,
                        f"You have {pending_count} pending order(s) waiting for processing. "
                        f"<a href='{reverse('supplier:view_orders')}?status=pending'>View pending orders</a>"
                    )
        
        # Process the response
        response = self.get_response(request)
        return response


class ShippedOrderReminderMiddleware:
    """
    Middleware to remind suppliers about orders that have been shipped but not delivered.
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Keep track of when we last checked for shipped orders
        self.last_check = {}  # Dict to track per supplier
    
    def __call__(self, request):
        # Only check for authenticated supplier users
        if (
            request.user.is_authenticated and 
            hasattr(request.user, 'profile') and 
            request.user.profile.role == SUPPLIER_ROLE and
            hasattr(request.user, 'supplier_profile')
        ):
            supplier = request.user.supplier_profile.supplier
            supplier_id = supplier.id
            
            # Check if we need to check for this supplier
            if (
                supplier_id not in self.last_check or 
                timezone.now() - self.last_check[supplier_id] > datetime.timedelta(days=1)
            ):
                # Update the last check time
                self.last_check[supplier_id] = timezone.now()
                
                # Check for shipped orders
                today = timezone.now().date()
                shipped_orders = Order.objects.filter(
                    supplier=supplier,
                    status='shipped',
                    expected_delivery__lte=today
                )
                
                shipped_count = shipped_orders.count()
                
                # Only add message if there are shipped orders past their expected delivery date
                if shipped_count > 0:
                    messages.warning(
                        request,
                        f"You have {shipped_count} shipped order(s) that have passed their expected delivery date. "
                        f"<a href='{reverse('supplier:view_orders')}?status=shipped'>Update these orders</a>"
                    )
        
        # Process the response
        response = self.get_response(request)
        return response