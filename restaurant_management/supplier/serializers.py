"""
Serializers for the supplier application.

These serializers convert complex data types (like Django models) to and from
Python data types that can be rendered into JSON or other formats.
"""

from rest_framework import serializers

from store.models import Order, OrderItem, Supplier
from .models import SupplierProfile, DeliveryNotification, SupplierPerformance


class SupplierProfileSerializer(serializers.ModelSerializer):
    """Serializer for SupplierProfile model."""
    
    username = serializers.SerializerMethodField()
    supplier_name = serializers.SerializerMethodField()
    
    class Meta:
        model = SupplierProfile
        fields = ['id', 'user', 'username', 'supplier', 'supplier_name']
    
    def get_username(self, obj):
        """Get the username of the user."""
        return obj.user.username
    
    def get_supplier_name(self, obj):
        """Get the name of the supplier."""
        return obj.supplier.name


class DeliveryNotificationSerializer(serializers.ModelSerializer):
    """Serializer for DeliveryNotification model."""
    
    order_id = serializers.SerializerMethodField()
    
    class Meta:
        model = DeliveryNotification
        fields = ['id', 'order', 'order_id', 'message', 'delivery_date', 'created_at', 'updated_at']
    
    def get_order_id(self, obj):
        """Get the ID of the order."""
        return obj.order.id


class SupplierPerformanceSerializer(serializers.ModelSerializer):
    """Serializer for SupplierPerformance model."""
    
    supplier_name = serializers.SerializerMethodField()
    on_time_percentage = serializers.SerializerMethodField()
    
    class Meta:
        model = SupplierPerformance
        fields = [
            'id', 'supplier', 'supplier_name', 'total_orders', 'on_time_deliveries',
            'late_deliveries', 'quality_rating', 'period_start', 'period_end',
            'on_time_percentage'
        ]
    
    def get_supplier_name(self, obj):
        """Get the name of the supplier."""
        return obj.supplier.name
    
    def get_on_time_percentage(self, obj):
        """Calculate the percentage of on-time deliveries."""
        return obj.on_time_percentage


class OrderItemSupplierSerializer(serializers.ModelSerializer):
    """Serializer for OrderItem model with supplier-specific fields."""
    
    item_name = serializers.SerializerMethodField()
    category = serializers.SerializerMethodField()
    
    class Meta:
        model = OrderItem
        fields = ['id', 'inventory', 'item_name', 'category', 'quantity_ordered']
    
    def get_item_name(self, obj):
        """Get the name of the inventory item."""
        return obj.inventory.item_name
    
    def get_category(self, obj):
        """Get the category of the inventory item."""
        return obj.inventory.category


class OrderSupplierSerializer(serializers.ModelSerializer):
    """Serializer for Order model with supplier-specific fields."""
    
    items = OrderItemSupplierSerializer(many=True, read_only=True, source='items.all')
    total_items = serializers.SerializerMethodField()
    delivery_notification = DeliveryNotificationSerializer(read_only=True)
    
    class Meta:
        model = Order
        fields = [
            'id', 'status', 'order_date', 'expected_delivery',
            'items', 'total_items', 'delivery_notification'
        ]
    
    def get_total_items(self, obj):
        """Get the total number of items in the order."""
        return sum(item.quantity_ordered for item in obj.items.all())


class SupplierDashboardSerializer(serializers.Serializer):
    """Serializer for supplier dashboard statistics."""
    
    pending_orders = serializers.IntegerField()
    shipped_orders = serializers.IntegerField()
    delivered_orders = serializers.IntegerField()
    total_orders = serializers.IntegerField()
    on_time_deliveries = serializers.IntegerField()
    on_time_percentage = serializers.FloatField()


class SupplierPerformanceHistorySerializer(serializers.Serializer):
    """Serializer for supplier performance history."""
    
    month = serializers.CharField()
    total_orders = serializers.IntegerField()
    on_time_deliveries = serializers.IntegerField()
    late_deliveries = serializers.IntegerField()
    on_time_percentage = serializers.FloatField()
    quality_rating = serializers.FloatField()