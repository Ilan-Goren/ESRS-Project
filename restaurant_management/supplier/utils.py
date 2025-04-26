"""
Utility functions for the supplier application.

This module contains helper functions and utilities for supplier-specific operations,
such as order management, delivery notifications, and performance metrics.
"""

import csv
import datetime
from io import BytesIO
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from django.http import HttpResponse
import xlsxwriter

from store.models import Order, OrderItem, Supplier
from .models import SupplierPerformance, DeliveryNotification


def calculate_supplier_metrics(supplier, start_date=None, end_date=None):
    """
    Calculate performance metrics for a specific supplier over a given time period.
    
    Args:
        supplier (Supplier): The supplier to calculate metrics for.
        start_date (date, optional): Start date for period. Defaults to 30 days ago.
        end_date (date, optional): End date for period. Defaults to today.
    
    Returns:
        dict: Dictionary containing supplier performance metrics.
    """
    # Set default period if not specified
    if not start_date:
        start_date = timezone.now().date() - datetime.timedelta(days=30)
    if not end_date:
        end_date = timezone.now().date()
    
    # Get relevant orders
    orders = Order.objects.filter(
        supplier=supplier,
        order_date__date__gte=start_date,
        order_date__date__lte=end_date
    )
    
    # Calculate metrics
    total_orders = orders.count()
    delivered_orders = orders.filter(status='delivered').count()
    cancelled_orders = orders.filter(status='cancelled').count()
    
    # On-time delivery calculation
    on_time_deliveries = 0
    late_deliveries = 0
    
    for order in orders.filter(status='delivered'):
        try:
            delivery_notification = order.delivery_notification
            if delivery_notification.delivery_date <= order.expected_delivery:
                on_time_deliveries += 1
            else:
                late_deliveries += 1
        except DeliveryNotification.DoesNotExist:
            # If no delivery notification exists, count based on status update timing
            if order.order_date.date() <= order.expected_delivery:
                on_time_deliveries += 1
            else:
                late_deliveries += 1
    
    # Calculate percentages
    on_time_percentage = 0
    if delivered_orders > 0:
        on_time_percentage = (on_time_deliveries / delivered_orders) * 100
    
    cancellation_rate = 0
    if total_orders > 0:
        cancellation_rate = (cancelled_orders / total_orders) * 100
    
    # Get or create performance record
    performance, created = SupplierPerformance.objects.get_or_create(
        supplier=supplier,
        period_start=start_date,
        period_end=end_date,
        defaults={
            'total_orders': total_orders,
            'on_time_deliveries': on_time_deliveries,
            'late_deliveries': late_deliveries,
            'quality_rating': 0.00
        }
    )
    
    # Update if it already exists
    if not created:
        performance.total_orders = total_orders
        performance.on_time_deliveries = on_time_deliveries
        performance.late_deliveries = late_deliveries
        performance.save()
    
    # Return metrics
    metrics = {
        'supplier': supplier,
        'performance': performance,
        'total_orders': total_orders,
        'delivered_orders': delivered_orders,
        'cancelled_orders': cancelled_orders,
        'on_time_deliveries': on_time_deliveries,
        'late_deliveries': late_deliveries,
        'on_time_percentage': on_time_percentage,
        'cancellation_rate': cancellation_rate,
        'period_start': start_date,
        'period_end': end_date,
    }
    
    return metrics


def get_supplier_order_summary(supplier, status=None, start_date=None, end_date=None):
    """
    Get a summary of orders for a supplier with filtering options.
    
    Args:
        supplier (Supplier): The supplier to get orders for.
        status (str, optional): Filter by order status. Defaults to None.
        start_date (date, optional): Filter by start date. Defaults to None.
        end_date (date, optional): Filter by end date. Defaults to None.
    
    Returns:
        QuerySet: Filtered orders for the supplier.
    """
    # Base query
    orders = Order.objects.filter(supplier=supplier)
    
    # Apply filters
    if status:
        orders = orders.filter(status=status)
    
    if start_date:
        orders = orders.filter(order_date__date__gte=start_date)
    
    if end_date:
        orders = orders.filter(order_date__date__lte=end_date)
    
    return orders.order_by('-order_date')


def export_supplier_orders(supplier, format_type='csv', status=None, start_date=None, end_date=None):
    """
    Export supplier orders data in the specified format.
    
    Args:
        supplier (Supplier): The supplier to export orders for.
        format_type (str): The format to export to ('csv' or 'excel').
        status (str, optional): Filter by order status. Defaults to None.
        start_date (date, optional): Filter by start date. Defaults to None.
        end_date (date, optional): Filter by end date. Defaults to None.
    
    Returns:
        HttpResponse: Response containing the exported data.
    """
    # Get filtered orders
    orders = get_supplier_order_summary(supplier, status, start_date, end_date)
    
    if format_type == 'csv':
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{supplier.name}_orders.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Order ID', 'Status', 'Order Date', 'Expected Delivery', 'Items', 'Total Quantity'])
        
        for order in orders:
            # Get order items info
            items_count = OrderItem.objects.filter(order=order).count()
            total_quantity = OrderItem.objects.filter(order=order).aggregate(
                total=Sum('quantity_ordered')
            )['total'] or 0
            
            writer.writerow([
                order.id,
                order.status,
                order.order_date.strftime('%Y-%m-%d %H:%M:%S'),
                order.expected_delivery.strftime('%Y-%m-%d') if order.expected_delivery else 'Not specified',
                items_count,
                total_quantity
            ])
        
        return response
    
    elif format_type == 'excel':
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        
        # Add header row
        headers = ['Order ID', 'Status', 'Order Date', 'Expected Delivery', 'Items', 'Total Quantity']
        
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#f0f0f0',
            'border': 1
        })
        
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, header_format)
        
        # Add data rows
        row_num = 1
        for order in orders:
            # Get order items info
            items_count = OrderItem.objects.filter(order=order).count()
            total_quantity = OrderItem.objects.filter(order=order).aggregate(
                total=Sum('quantity_ordered')
            )['total'] or 0
            
            worksheet.write(row_num, 0, order.id)
            worksheet.write(row_num, 1, order.status)
            worksheet.write(row_num, 2, order.order_date.strftime('%Y-%m-%d %H:%M:%S'))
            
            if order.expected_delivery:
                worksheet.write(row_num, 3, order.expected_delivery.strftime('%Y-%m-%d'))
            else:
                worksheet.write(row_num, 3, 'Not specified')
            
            worksheet.write(row_num, 4, items_count)
            worksheet.write(row_num, 5, total_quantity)
            
            row_num += 1
        
        # Adjust column widths
        for col_num, header in enumerate(headers):
            worksheet.set_column(col_num, col_num, len(header) + 5)
        
        workbook.close()
        output.seek(0)
        
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{supplier.name}_orders.xlsx"'
        
        return response
    
    # Default to CSV if format not recognized
    return export_supplier_orders(supplier, 'csv', status, start_date, end_date)


def calculate_monthly_performance_history(supplier, months=6):
    """
    Calculate performance metrics for a supplier over the past X months.
    
    Args:
        supplier (Supplier): The supplier to calculate metrics for.
        months (int, optional): Number of months to include. Defaults to 6.
    
    Returns:
        list: List of dictionaries containing monthly performance data.
    """
    today = timezone.now().date()
    performance_history = []
    
    for i in range(months):
        # Calculate month period
        end_date = today.replace(day=1) - datetime.timedelta(days=1) - datetime.timedelta(days=30*i)
        start_date = end_date.replace(day=1)
        
        # Get or calculate performance
        try:
            performance = SupplierPerformance.objects.get(
                supplier=supplier,
                period_start=start_date,
                period_end=end_date
            )
            
            # Get data from existing record
            metrics = {
                'month': start_date.strftime('%b %Y'),
                'period_start': start_date,
                'period_end': end_date,
                'total_orders': performance.total_orders,
                'on_time_deliveries': performance.on_time_deliveries,
                'late_deliveries': performance.late_deliveries,
                'quality_rating': performance.quality_rating,
            }
            
        except SupplierPerformance.DoesNotExist:
            # Calculate metrics for this period
            metrics_data = calculate_supplier_metrics(supplier, start_date, end_date)
            
            metrics = {
                'month': start_date.strftime('%b %Y'),
                'period_start': start_date,
                'period_end': end_date,
                'total_orders': metrics_data['total_orders'],
                'on_time_deliveries': metrics_data['on_time_deliveries'],
                'late_deliveries': metrics_data['late_deliveries'],
                'quality_rating': 0.00,
            }
        
        # Calculate on-time percentage
        if metrics['total_orders'] > 0:
            metrics['on_time_percentage'] = (metrics['on_time_deliveries'] / metrics['total_orders']) * 100
        else:
            metrics['on_time_percentage'] = 0
        
        performance_history.append(metrics)
    
    # Reverse to get chronological order
    performance_history.reverse()
    
    return performance_history