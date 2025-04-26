"""
Serializers for the store application.

These serializers convert complex data types (like Django models) to and from
Python data types that can be rendered into JSON or other formats.
"""

from rest_framework import serializers

from .models import Inventory, Order, OrderItem, Transaction, Supplier, UserProfile


class SupplierSerializer(serializers.ModelSerializer):
    """Serializer for Supplier model."""
    
    class Meta:
        model = Supplier
        fields = ['id', 'name', 'contact_info', 'email', 'phone', 'created_at']


class InventorySerializer(serializers.ModelSerializer):
    """Serializer for Inventory model."""
    
    supplier_name = serializers.SerializerMethodField()
    is_low_stock = serializers.SerializerMethodField()
    is_expired = serializers.SerializerMethodField()
    
    class Meta:
        model = Inventory
        fields = [
            'id', 'sku', 'item_name', 'category', 'quantity', 'reorder_level',
            'expiry_date', 'supplier', 'supplier_name', 'last_updated',
            'is_low_stock', 'is_expired'
        ]
    
    def get_supplier_name(self, obj):
        """Get the name of the supplier."""
        return obj.supplier.name if obj.supplier else None
    
    def get_is_low_stock(self, obj):
        """Check if the item is low in stock."""
        return obj.is_low_stock
    
    def get_is_expired(self, obj):
        """Check if the item is expired."""
        return obj.is_expired


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model."""
    
    item_name = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'order', 'inventory', 'item_name', 'quantity_ordered']
    
    def get_item_name(self, obj):
        """Get the name of the inventory item."""
        return obj.inventory.item_name


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model."""
    
    supplier_name = serializers.SerializerMethodField()
    items = OrderItemSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    
    class Meta:
        model = Order
        fields = [
            'id', 'supplier', 'supplier_name', 'status', 'order_date',
            'expected_delivery', 'items', 'total_items'
        ]
    
    def get_supplier_name(self, obj):
        """Get the name of the supplier."""
        return obj.supplier.name
    
    def get_total_items(self, obj):
        """Get the total number of items in the order."""
        return sum(item.quantity_ordered for item in obj.items.all())


class TransactionSerializer(serializers.ModelSerializer):
    """Serializer for Transaction model."""
    
    item_name = serializers.SerializerMethodField()
    username = serializers.SerializerMethodField()
    
    class Meta:
        model = Transaction
        fields = [
            'id', 'inventory', 'item_name', 'user', 'username',
            'quantity_used', 'transaction_type', 'created_at'
        ]
    
    def get_item_name(self, obj):
        """Get the name of the inventory item."""
        return obj.inventory.item_name
    
    def get_username(self, obj):
        """Get the username of the user who made the transaction."""
        return obj.user.user.username


class UserProfileSerializer(serializers.ModelSerializer):
    """Serializer for UserProfile model."""
    
    username = serializers.SerializerMethodField()
    email = serializers.SerializerMethodField()
    
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'username', 'email', 'role', 'created_at']
    
    def get_username(self, obj):
        """Get the username of the user."""
        return obj.user.username
    
    def get_email(self, obj):
        """Get the email of the user."""
        return obj.user.email


class DashboardStatsSerializer(serializers.Serializer):
    """Serializer for dashboard statistics."""
    
    total_inventory_items = serializers.IntegerField()
    total_inventory_value = serializers.IntegerField()
    low_stock_count = serializers.IntegerField()
    expiring_count = serializers.IntegerField()
    expired_count = serializers.IntegerField()
    pending_orders = serializers.IntegerField()
    shipped_orders = serializers.IntegerField()
    delivered_orders = serializers.IntegerField()
    added_today = serializers.IntegerField()
    removed_today = serializers.IntegerField()


class InventoryCategorySerializer(serializers.Serializer):
    """Serializer for inventory category statistics."""
    
    category = serializers.CharField(allow_null=True)
    total = serializers.IntegerField()
    total_quantity = serializers.IntegerField()