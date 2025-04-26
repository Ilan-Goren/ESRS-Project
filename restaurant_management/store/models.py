"""
Models for the store application.

These models directly correspond to the tables in the database schema.
The models use Django's ORM and mirror the structure provided in the restaurant_inventory.sql file.
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserProfile(models.Model):
    """
    Extends the built-in Django User model with additional fields for role-based access.
    Maps to the 'users' table in the database.
    """
    USER_ROLES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
        ('supplier', 'Supplier'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    role = models.CharField(max_length=20, choices=USER_ROLES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.role}"

    class Meta:
        db_table = 'users'
        managed = False  # Using existing database table
        
    @property
    def is_admin(self):
        return self.role == 'admin'
        
    @property
    def is_manager(self):
        return self.role == 'manager'
        
    @property
    def is_staff(self):
        return self.role == 'staff'
        
    @property
    def is_supplier(self):
        return self.role == 'supplier'


class Supplier(models.Model):
    """
    Represents a supplier who provides inventory items.
    Maps to the 'suppliers' table in the database.
    """
    name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'suppliers'
        managed = False  # Using existing database table


class Inventory(models.Model):
    """
    Represents inventory items in stock.
    Maps to the 'inventory' table in the database.
    """
    sku = models.CharField(max_length=50, unique=True, blank=True, null=True)
    item_name = models.CharField(max_length=255)
    category = models.CharField(max_length=100, blank=True, null=True)
    quantity = models.IntegerField(default=0)
    reorder_level = models.IntegerField()
    expiry_date = models.DateField(blank=True, null=True)
    supplier = models.ForeignKey(Supplier, on_delete=models.SET_NULL, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.item_name} - {self.quantity} units"
    
    class Meta:
        db_table = 'inventory'
        managed = False  # Using existing database table
        verbose_name_plural = "Inventory Items"
        indexes = [
            models.Index(fields=['item_name']),
        ]
    
    @property
    def is_low_stock(self):
        """Check if the inventory item is below reorder level."""
        return self.quantity <= self.reorder_level
    
    @property
    def is_expired(self):
        """Check if the inventory item is expired."""
        if self.expiry_date:
            return self.expiry_date < timezone.now().date()
        return False


class Order(models.Model):
    """
    Represents orders placed with suppliers.
    Maps to the 'orders' table in the database.
    """
    ORDER_STATUS = (
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    status = models.CharField(max_length=10, choices=ORDER_STATUS, default='pending')
    order_date = models.DateTimeField(default=timezone.now)
    expected_delivery = models.DateField(blank=True, null=True)
    
    def __str__(self):
        return f"Order #{self.id} - {self.supplier.name} - {self.status}"
    
    class Meta:
        db_table = 'orders'
        managed = False  # Using existing database table


class OrderItem(models.Model):
    """
    Represents individual items within an order.
    Maps to the 'order_items' table in the database.
    """
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    quantity_ordered = models.IntegerField()
    
    def __str__(self):
        return f"{self.inventory.item_name} - {self.quantity_ordered} units"
    
    class Meta:
        db_table = 'order_items'
        managed = False  # Using existing database table


class Transaction(models.Model):
    """
    Tracks all transactions related to inventory items.
    Maps to the 'transactions' table in the database.
    """
    TRANSACTION_TYPES = (
        ('added', 'Added'),
        ('removed', 'Removed'),
        ('adjusted', 'Adjusted'),
    )
    
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE)
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    quantity_used = models.IntegerField()
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.transaction_type} {self.quantity_used} of {self.inventory.item_name}"
    
    class Meta:
        db_table = 'transactions'
        managed = False  # Using existing database table