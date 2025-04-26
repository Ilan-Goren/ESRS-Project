"""
Context processors for the restaurant management system.

These functions add variables to the template context for all templates.
"""

from store.models import Inventory
from django.db.models import Sum, Count, F


def global_stats(request):
    """
    Add global statistics to the template context.
    
    This makes basic inventory statistics available to all templates.
    
    Args:
        request: The current HTTP request.
    
    Returns:
        dict: Dictionary containing global statistics.
    """
    # Only compute stats for authenticated users
    if not request.user.is_authenticated:
        return {}
    
    # Initial empty context
    context = {}
    
    try:
        # Get inventory counts
        total_inventory = Inventory.objects.count()
        low_stock_count = Inventory.objects.filter(quantity__lte=F('reorder_level')).count()
        
        # Add to context
        context.update({
            'total_inventory': total_inventory,
            'low_stock_count': low_stock_count,
        })
    except Exception:
        # If there's an error (e.g., database not yet set up), return empty context
        pass
    
    return context


def user_role(request):
    """
    Add user role information to the template context.
    
    This makes the user's role available to all templates.
    
    Args:
        request: The current HTTP request.
    
    Returns:
        dict: Dictionary containing user role information.
    """
    context = {
        'is_admin': False,
        'is_manager': False,
        'is_staff': False,
        'is_supplier': False,
    }
    
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            role = profile.role
            
            context.update({
                'user_role': role,
                'is_admin': role == 'admin',
                'is_manager': role == 'manager',
                'is_staff': role == 'staff',
                'is_supplier': role == 'supplier',
            })
        except Exception:
            # If profile doesn't exist, leave defaults
            pass
    
    return context