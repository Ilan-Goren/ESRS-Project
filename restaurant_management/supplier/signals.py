"""
Signal handlers for the supplier application.

These signals help maintain data integrity and automate certain processes
specific to supplier operations.
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.db.models import Count, Q, F

from store.models import Order, Supplier
from .models import DeliveryNotification, SupplierPerformance


@receiver(post_save, sender=DeliveryNotification)
def update_order_status_on_notification(sender, instance, created, **kwargs):
    """
    Update the associated order's status when a delivery notification is created or updated.
    
    Args:
        sender: The model class (DeliveryNotification).
        instance: The DeliveryNotification instance that was saved.
        created: Boolean flag indicating if the instance was created.
    """
    order = instance.order
    
    # If the delivery date is today or in the past, mark as delivered
    if instance.delivery_date <= timezone.now().date() and order.status != 'delivered':
        order.status = 'delivered'
        order.save(update_fields=['status'])
    # If the delivery date is in the future, mark as shipped if not already delivered
    elif order.status == 'pending':
        order.status = 'shipped'
        order.save(update_fields=['status'])


@receiver(post_save, sender=Order)
def update_supplier_performance(sender, instance, **kwargs):
    """
    Update or create supplier performance metrics when an order status changes.
    
    Args:
        sender: The model class (Order).
        instance: The Order instance that was saved.
    """
    supplier = instance.supplier
    
    # Only update performance metrics for delivered orders
    if instance.status == 'delivered':
        # Get the current month's start and end dates
        today = timezone.now().date()
        month_start = today.replace(day=1)
        next_month = today + relativedelta(months=1)
        month_end = next_month.replace(day=1) - relativedelta(days=1)
        
        # Get or create performance record for current month
        performance, created = SupplierPerformance.objects.get_or_create(
            supplier=supplier,
            period_start=month_start,
            period_end=month_end,
            defaults={
                'total_orders': 0,
                'on_time_deliveries': 0,
                'late_deliveries': 0,
                'quality_rating': 0.00
            }
        )
        
        # Increment total orders if this is the first time the order was marked as delivered
        try:
            old_status = Order.objects.get(pk=instance.pk).status
            if old_status != 'delivered':
                performance.total_orders += 1
                
                # Check if delivery was on time
                if hasattr(instance, 'delivery_notification'):
                    delivery_date = instance.delivery_notification.delivery_date
                    if delivery_date <= instance.expected_delivery:
                        performance.on_time_deliveries += 1
                    else:
                        performance.late_deliveries += 1
                
                performance.save()
        except Order.DoesNotExist:
            # New order, shouldn't happen in this context but handle it anyway
            pass


@receiver(post_save, sender=Supplier)
def initialize_supplier_performance(sender, instance, created, **kwargs):
    """
    Initialize performance metrics for a new supplier.
    
    Args:
        sender: The model class (Supplier).
        instance: The Supplier instance that was saved.
        created: Boolean flag indicating if the instance was created.
    """
    if created:
        # Get the current month's start and end dates
        today = timezone.now().date()
        month_start = today.replace(day=1)
        next_month = today + relativedelta(months=1)
        month_end = next_month.replace(day=1) - relativedelta(days=1)
        
        # Create initial performance record
        SupplierPerformance.objects.create(
            supplier=instance,
            period_start=month_start,
            period_end=month_end,
            total_orders=0,
            on_time_deliveries=0,
            late_deliveries=0,
            quality_rating=0.00
        )