"""
Django admin configuration for the supplier application.
"""

from django.contrib import admin

from .models import SupplierProfile, DeliveryNotification, SupplierPerformance


@admin.register(SupplierProfile)
class SupplierProfileAdmin(admin.ModelAdmin):
    """Admin configuration for SupplierProfile model."""
    list_display = ('user', 'supplier')
    search_fields = ('user__username', 'supplier__name')
    raw_id_fields = ('user', 'supplier')


@admin.register(DeliveryNotification)
class DeliveryNotificationAdmin(admin.ModelAdmin):
    """Admin configuration for DeliveryNotification model."""
    list_display = ('order', 'delivery_date', 'created_at')
    search_fields = ('order__id', 'message')
    raw_id_fields = ('order',)
    readonly_fields = ('created_at', 'updated_at')


@admin.register(SupplierPerformance)
class SupplierPerformanceAdmin(admin.ModelAdmin):
    """Admin configuration for SupplierPerformance model."""
    list_display = ('supplier', 'period_start', 'period_end', 'total_orders', 
                   'on_time_deliveries', 'late_deliveries', 'quality_rating', 'on_time_percentage')
    list_filter = ('supplier', 'period_start', 'period_end')
    search_fields = ('supplier__name',)
    
    def on_time_percentage(self, obj):
        """Calculate and display the on-time delivery percentage."""
        return f"{obj.on_time_percentage:.2f}%"
    on_time_percentage.short_description = 'On-time %'