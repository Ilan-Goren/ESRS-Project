"""
Django admin configuration for the store application.
"""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from .models import UserProfile, Inventory, Order, OrderItem, Transaction, Supplier


class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile."""
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'User Profiles'


class CustomUserAdmin(UserAdmin):
    """Custom User admin that includes the UserProfile inline."""
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'get_role', 'is_staff')
    
    def get_role(self, obj):
        try:
            return obj.profile.role
        except UserProfile.DoesNotExist:
            return 'No profile'
    get_role.short_description = 'Role'


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)


class OrderItemInline(admin.TabularInline):
    """Inline admin for OrderItems."""
    model = OrderItem
    extra = 1
    readonly_fields = ('inventory',)


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    """Admin configuration for Inventory model."""
    list_display = ('item_name', 'category', 'quantity', 'reorder_level', 'is_low_stock', 'supplier', 'expiry_date')
    list_filter = ('category', 'supplier')
    search_fields = ('item_name', 'sku')
    readonly_fields = ('last_updated',)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('supplier')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    """Admin configuration for Order model."""
    list_display = ('id', 'supplier', 'status', 'order_date', 'expected_delivery')
    list_filter = ('status', 'supplier')
    search_fields = ('id', 'supplier__name')
    inlines = [OrderItemInline]
    readonly_fields = ('order_date',)


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    """Admin configuration for Transaction model."""
    list_display = ('inventory', 'user', 'quantity_used', 'transaction_type', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('inventory__item_name', 'user__user__username')
    readonly_fields = ('created_at',)
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.select_related('inventory', 'user__user')


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    """Admin configuration for Supplier model."""
    list_display = ('name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email', 'phone')
    readonly_fields = ('created_at',)