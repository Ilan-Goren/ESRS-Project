"""
Models for the supplier application.

These models connect to the same database as the store app but are specifically
designed for the supplier interface. They reuse the tables defined in the
restaurant_inventory.sql file but with a supplier-focused perspective.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Import models from store app to maintain relationship consistency
from store.models import Supplier, Order, OrderItem, Inventory


class SupplierProfile(models.Model):
    """
    Extension of the UserProfile model specifically for supplier users.
    This provides a clean interface for supplier-specific functionality.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='supplier_profile')
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='profiles')
    
    def __str__(self):
        return f"Supplier Profile: {self.user.username} - {self.supplier.name}"
    
    class Meta:
        verbose_name = "Supplier Profile"
        verbose_name_plural = "Supplier Profiles"


class SupplierOrder(models.Model):
    """
    Proxy model for Order, providing supplier-specific methods and properties.
    This doesn't create a new table but provides a different interface to the orders table.
    """
    class Meta:
        proxy = True
        verbose_name = "Supplier Order"
        verbose_name_plural = "Supplier Orders"

    @classmethod
    def get_pending_orders(cls, supplier_id):
        """Get all pending orders for a specific supplier."""
        return Order.objects.filter(supplier_id=supplier_id, status='pending')
    
    @classmethod
    def get_shipped_orders(cls, supplier_id):
        """Get all shipped orders for a specific supplier."""
        return Order.objects.filter(supplier_id=supplier_id, status='shipped')
    
    @classmethod
    def get_delivered_orders(cls, supplier_id):
        """Get all delivered orders for a specific supplier."""
        return Order.objects.filter(supplier_id=supplier_id, status='delivered')
    
    @classmethod
    def get_all_orders(cls, supplier_id):
        """Get all orders for a specific supplier."""
        return Order.objects.filter(supplier_id=supplier_id)


class DeliveryNotification(models.Model):
    """
    Additional model to track delivery notifications from suppliers.
    This supplements the core schema with supplier-specific functionality.
    """
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='delivery_notification')
    message = models.TextField(blank=True, null=True)
    delivery_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"Delivery notification for Order #{self.order.id}"


class SupplierPerformance(models.Model):
    """
    Model to track supplier performance metrics.
    This is a custom extension to the core schema for analytics purposes.
    """
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name='performance_metrics')
    total_orders = models.IntegerField(default=0)
    on_time_deliveries = models.IntegerField(default=0)
    late_deliveries = models.IntegerField(default=0)
    quality_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    period_start = models.DateField()
    period_end = models.DateField()
    
    def __str__(self):
        return f"Performance: {self.supplier.name} ({self.period_start} to {self.period_end})"
    
    @property
    def on_time_percentage(self):
        """Calculate percentage of on-time deliveries."""
        if self.total_orders == 0:
            return 0
        return (self.on_time_deliveries / self.total_orders) * 100
    
    class Meta:
        unique_together = ('supplier', 'period_start', 'period_end')