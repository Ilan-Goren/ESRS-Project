"""
Signal handlers for the store application.

These signals help maintain data integrity and automate certain processes
when database operations occur.
"""

from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils import timezone

from .models import UserProfile, Inventory, Order, OrderItem, Transaction


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """
    Create a UserProfile when a new User is created.
    
    Args:
        sender: The model class (User).
        instance: The User instance that was saved.
        created: Boolean flag indicating if the instance was created.
    """
    if created:
        # Create a default staff profile if one doesn't exist
        UserProfile.objects.get_or_create(user=instance, defaults={'role': 'staff'})


@receiver(post_save, sender=OrderItem)
def update_inventory_on_order(sender, instance, created, **kwargs):
    """
    Update inventory quantities when an order item is created.
    This is complementary to the database trigger but ensures Django is aware of the changes.
    
    Args:
        sender: The model class (OrderItem).
        instance: The OrderItem instance that was saved.
        created: Boolean flag indicating if the instance was created.
    """
    if created:
        # The database trigger will handle the actual quantity reduction
        # But we need to make sure Django's ORM is aware of the change
        inventory = instance.inventory
        inventory.refresh_from_db()  # Refresh to get the updated quantity after trigger


@receiver(post_save, sender=Transaction)
def update_inventory_on_transaction(sender, instance, created, **kwargs):
    """
    Update inventory last_updated timestamp when a transaction occurs.
    
    Args:
        sender: The model class (Transaction).
        instance: The Transaction instance that was saved.
        created: Boolean flag indicating if the instance was created.
    """
    if created:
        inventory = instance.inventory
        inventory.last_updated = timezone.now()
        inventory.save(update_fields=['last_updated'])


@receiver(pre_save, sender=Order)
def check_order_status_change(sender, instance, **kwargs):
    """
    Perform actions when an order's status changes.
    
    Args:
        sender: The model class (Order).
        instance: The Order instance being saved.
    """
    try:
        old_instance = Order.objects.get(pk=instance.pk)
        
        # If status changed from something else to 'delivered'
        if old_instance.status != 'delivered' and instance.status == 'delivered':
            # Record the delivery date if not already set
            if not hasattr(instance, 'delivery_notification'):
                from supplier.models import DeliveryNotification
                DeliveryNotification.objects.create(
                    order=instance,
                    delivery_date=timezone.now().date(),
                    message="Order automatically marked as delivered."
                )
    except Order.DoesNotExist:
        # This is a new order, no previous status to compare
        pass