from django.db import models
from store.models import Supplier, Order, OrderItem

# We are extending the store models with supplier-specific methods

class SupplierManager(models.Manager):
    """Custom manager for suppliers to add supplier-specific functionality"""
    
    def get_pending_orders(self, supplier_id):
        """Get all pending orders for a supplier"""
        return Order.objects.filter(supplier_id=supplier_id, status='pending')
    
    def get_orders_by_status(self, supplier_id, status):
        """Get orders for a supplier filtered by status"""
        return Order.objects.filter(supplier_id=supplier_id, status=status)
    
    def get_all_orders(self, supplier_id):
        """Get all orders for a supplier"""
        return Order.objects.filter(supplier_id=supplier_id)

class SupplierExtended(Supplier):
    """
    Proxy model for Supplier to add supplier-specific methods
    This doesn't create a new table but extends the existing Supplier model
    """
    objects = SupplierManager()
    
    class Meta:
        proxy = True
        
    def get_pending_orders(self):
        """Get all pending orders for this supplier"""
        return Order.objects.filter(supplier=self, status='pending')
    
    def get_orders_by_status(self, status):
        """Get orders for this supplier filtered by status"""
        return Order.objects.filter(supplier=self, status=status)
    
    def get_all_orders(self):
        """Get all orders for this supplier"""
        return Order.objects.filter(supplier=self)
    
    def get_recent_orders(self, days=30):
        """Get recent orders within specified days"""
        from django.utils import timezone
        import datetime
        
        cutoff_date = timezone.now() - datetime.timedelta(days=days)
        return Order.objects.filter(supplier=self, order_date__gte=cutoff_date)