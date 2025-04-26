"""
Custom template tags and filters for the supplier application.
"""

from django import template
from django.utils import timezone
import datetime

register = template.Library()


@register.filter
def performance_color(percentage):
    """
    Return the appropriate Bootstrap color class based on performance percentage.
    
    Args:
        percentage (float): Performance percentage value.
    
    Returns:
        str: Bootstrap color class.
    """
    if percentage >= 90:
        return 'success'
    elif percentage >= 75:
        return 'info'
    elif percentage >= 50:
        return 'warning'
    else:
        return 'danger'


@register.filter
def on_time_status(order):
    """
    Check if an order is on track to be delivered on time.
    
    Args:
        order: Order object.
    
    Returns:
        str: Status indicator ('on-time', 'at-risk', 'late').
    """
    if not order.expected_delivery:
        return 'unknown'
    
    today = timezone.now().date()
    
    if order.status == 'delivered':
        try:
            delivery_notification = order.delivery_notification
            if delivery_notification.delivery_date <= order.expected_delivery:
                return 'on-time'
            else:
                return 'late'
        except Exception:
            return 'unknown'
    
    elif order.status == 'cancelled':
        return 'cancelled'
    
    elif order.expected_delivery < today:
        return 'late'
    
    elif (order.expected_delivery - today).days <= 2:
        return 'at-risk'
    
    return 'on-time'


@register.filter
def delivery_status_color(status):
    """
    Return the appropriate Bootstrap color class for a delivery status.
    
    Args:
        status (str): Delivery status string.
    
    Returns:
        str: Bootstrap color class.
    """
    status_colors = {
        'on-time': 'success',
        'at-risk': 'warning',
        'late': 'danger',
        'cancelled': 'secondary',
        'unknown': 'info',
    }
    
    return status_colors.get(status, 'secondary')


@register.filter
def order_count_color(count):
    """
    Return the appropriate Bootstrap color class based on order count.
    
    Args:
        count (int): Order count.
    
    Returns:
        str: Bootstrap color class.
    """
    if count <= 0:
        return 'secondary'
    elif count < 5:
        return 'info'
    elif count < 10:
        return 'warning'
    else:
        return 'danger'


@register.simple_tag
def active_orders_count(supplier):
    """
    Count active orders for a supplier.
    
    Args:
        supplier: Supplier object.
    
    Returns:
        int: Count of active orders.
    """
    from store.models import Order
    
    return Order.objects.filter(
        supplier=supplier,
        status__in=['pending', 'shipped']
    ).count()


@register.simple_tag
def calculate_completion_rate(supplier):
    """
    Calculate the order completion rate for a supplier.
    
    Args:
        supplier: Supplier object.
    
    Returns:
        float: Completion rate as a percentage.
    """
    from store.models import Order
    
    total_orders = Order.objects.filter(supplier=supplier).count()
    
    if total_orders == 0:
        return 0
    
    completed_orders = Order.objects.filter(
        supplier=supplier,
        status='delivered'
    ).count()
    
    return (completed_orders / total_orders) * 100