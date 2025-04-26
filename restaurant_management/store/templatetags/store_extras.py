"""
Custom template tags and filters for the store application.
"""

from django import template
from django.utils import timezone
import datetime

register = template.Library()


@register.filter
def status_color(status):
    """
    Return the appropriate Bootstrap color class for an order status.
    
    Args:
        status (str): Order status string.
    
    Returns:
        str: Bootstrap color class.
    """
    status_colors = {
        'pending': 'warning',
        'shipped': 'info',
        'delivered': 'success',
        'cancelled': 'danger',
    }
    
    return status_colors.get(status, 'secondary')


@register.filter
def quantity_color(item):
    """
    Return the appropriate Bootstrap color class for an inventory item's quantity.
    
    Args:
        item: Inventory item object.
    
    Returns:
        str: Bootstrap color class.
    """
    if item.quantity <= 0:
        return 'danger'
    elif item.quantity <= item.reorder_level:
        return 'warning'
    else:
        return 'success'


@register.filter
def days_until(date):
    """
    Calculate the number of days until a future date.
    
    Args:
        date: Future date object.
    
    Returns:
        int: Number of days, or None if date is None.
    """
    if not date:
        return None
    
    today = timezone.now().date()
    delta = date - today
    
    return delta.days


@register.filter
def days_ago(date):
    """
    Calculate the number of days since a past date.
    
    Args:
        date: Past date object.
    
    Returns:
        int: Number of days, or None if date is None.
    """
    if not date:
        return None
    
    today = timezone.now().date()
    delta = today - date
    
    return delta.days


@register.filter
def multiply(value, arg):
    """
    Multiply the value by the argument.
    
    Args:
        value: First value.
        arg: Second value.
    
    Returns:
        float: Product of the two values.
    """
    try:
        return float(value) * float(arg)
    except (ValueError, TypeError):
        return 0


@register.simple_tag
def get_verbose_name(instance, field_name):
    """
    Return the verbose name of a model field.
    
    Args:
        instance: Model instance.
        field_name: Name of the field.
    
    Returns:
        str: Verbose name of the field.
    """
    return instance._meta.get_field(field_name).verbose_name.title()


@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Return encoded URL parameters that are the same as the current request's 
    parameters, only with the specified parameters modified.
    
    Args:
        context: Template context.
        **kwargs: Parameters to modify.
    
    Returns:
        str: Encoded URL parameters.
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()