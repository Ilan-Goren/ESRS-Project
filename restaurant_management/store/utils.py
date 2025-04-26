"""
Utility functions for the store application.

This module contains helper functions and utilities for inventory management,
order processing, and reporting functionality.
"""

import csv
import datetime
from io import StringIO, BytesIO
from django.db.models import Sum, Count, Q, F
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string
import xlsxwriter

from restaurant_management.utils.constants import (
    LOW_STOCK_WARNING_DAYS, EXPIRY_WARNING_DAYS,
    PDF_EXPORT, CSV_EXPORT, EXCEL_EXPORT
)
from .models import Inventory, Order, OrderItem, Transaction, Supplier


def get_low_stock_items():
    """
    Get inventory items that are at or below their reorder level.
    
    Returns:
        QuerySet: All inventory items that need to be reordered.
    """
    return Inventory.objects.filter(quantity__lte=F('reorder_level'))


def get_expiring_items(days=EXPIRY_WARNING_DAYS):
    """
    Get inventory items that will expire within the specified number of days.
    
    Args:
        days (int): Number of days threshold for expiry warning.
    
    Returns:
        QuerySet: All inventory items expiring within the specified days.
    """
    today = timezone.now().date()
    expiry_threshold = today + datetime.timedelta(days=days)
    
    return Inventory.objects.filter(
        expiry_date__isnull=False,
        expiry_date__lte=expiry_threshold,
        expiry_date__gte=today
    )


def get_expired_items():
    """
    Get inventory items that have already expired.
    
    Returns:
        QuerySet: All expired inventory items.
    """
    today = timezone.now().date()
    
    return Inventory.objects.filter(
        expiry_date__isnull=False,
        expiry_date__lt=today
    )


def get_dashboard_stats(user=None):
    """
    Get statistics for dashboard display.
    
    Args:
        user (User, optional): User to filter transactions by. Defaults to None.
    
    Returns:
        dict: Dictionary containing dashboard statistics.
    """
    # Count inventory stats
    total_inventory_items = Inventory.objects.count()
    total_inventory_value = Inventory.objects.aggregate(
        total_quantity=Sum('quantity')
    )['total_quantity'] or 0
    
    low_stock_count = get_low_stock_items().count()
    expiring_count = get_expiring_items().count()
    expired_count = get_expired_items().count()
    
    # Count order stats
    pending_orders = Order.objects.filter(status='pending').count()
    shipped_orders = Order.objects.filter(status='shipped').count()
    delivered_orders = Order.objects.filter(status='delivered').count()
    
    # Get transaction stats
    transactions_today = Transaction.objects.filter(
        created_at__date=timezone.now().date()
    )
    
    if user:
        transactions_today = transactions_today.filter(user__user=user)
    
    added_today = transactions_today.filter(
        transaction_type='added'
    ).aggregate(total=Sum('quantity_used'))['total'] or 0
    
    removed_today = transactions_today.filter(
        transaction_type='removed'
    ).aggregate(total=Sum('quantity_used'))['total'] or 0
    
    # Inventory by category
    inventory_by_category = Inventory.objects.values('category').annotate(
        total=Count('id'),
        total_quantity=Sum('quantity')
    )
    
    stats = {
        'total_inventory_items': total_inventory_items,
        'total_inventory_value': total_inventory_value,
        'low_stock_count': low_stock_count,
        'expiring_count': expiring_count,
        'expired_count': expired_count,
        'pending_orders': pending_orders,
        'shipped_orders': shipped_orders,
        'delivered_orders': delivered_orders,
        'added_today': added_today,
        'removed_today': removed_today,
        'inventory_by_category': inventory_by_category,
    }
    
    return stats


def export_inventory_report(format_type=CSV_EXPORT):
    """
    Export inventory data in the specified format.
    
    Args:
        format_type (str): The format to export to (pdf, csv, excel).
    
    Returns:
        HttpResponse: Response containing the exported data.
    """
    inventory_items = Inventory.objects.select_related('supplier').all()
    
    if format_type == CSV_EXPORT:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="inventory_report.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['ID', 'SKU', 'Item Name', 'Category', 'Quantity', 
                        'Reorder Level', 'Expiry Date', 'Supplier', 'Last Updated'])
        
        for item in inventory_items:
            writer.writerow([
                item.id,
                item.sku or '',
                item.item_name,
                item.category or '',
                item.quantity,
                item.reorder_level,
                item.expiry_date.strftime('%Y-%m-%d') if item.expiry_date else '',
                item.supplier.name if item.supplier else '',
                item.last_updated.strftime('%Y-%m-%d %H:%M:%S')
            ])
        
        return response
    
    elif format_type == EXCEL_EXPORT:
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        
        # Add header row
        headers = ['ID', 'SKU', 'Item Name', 'Category', 'Quantity', 
                  'Reorder Level', 'Expiry Date', 'Supplier', 'Last Updated']
        
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#f0f0f0',
            'border': 1
        })
        
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, header_format)
        
        # Add data rows
        row_num = 1
        for item in inventory_items:
            worksheet.write(row_num, 0, item.id)
            worksheet.write(row_num, 1, item.sku or '')
            worksheet.write(row_num, 2, item.item_name)
            worksheet.write(row_num, 3, item.category or '')
            worksheet.write(row_num, 4, item.quantity)
            worksheet.write(row_num, 5, item.reorder_level)
            
            if item.expiry_date:
                worksheet.write(row_num, 6, item.expiry_date.strftime('%Y-%m-%d'))
            else:
                worksheet.write(row_num, 6, '')
            
            worksheet.write(row_num, 7, item.supplier.name if item.supplier else '')
            worksheet.write(row_num, 8, item.last_updated.strftime('%Y-%m-%d %H:%M:%S'))
            
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
        response['Content-Disposition'] = 'attachment; filename="inventory_report.xlsx"'
        
        return response
    
    # PDF export implementation using WeasyPrint or another PDF generation library
    # would go here if implemented
    
    # Default to CSV if format not recognized
    return export_inventory_report(CSV_EXPORT)


def export_order_report(start_date, end_date, format_type=CSV_EXPORT):
    """
    Export order data for a date range in the specified format.
    
    Args:
        start_date (date): Start date for report period.
        end_date (date): End date for report period.
        format_type (str): The format to export to (pdf, csv, excel).
    
    Returns:
        HttpResponse: Response containing the exported data.
    """
    orders = Order.objects.filter(
        order_date__date__gte=start_date,
        order_date__date__lte=end_date
    ).select_related('supplier')
    
    if format_type == CSV_EXPORT:
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="order_report_{start_date}_{end_date}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Order ID', 'Supplier', 'Status', 'Order Date', 
                        'Expected Delivery', 'Items Count', 'Total Items'])
        
        for order in orders:
            # Get order items info
            items_count = OrderItem.objects.filter(order=order).count()
            total_items = OrderItem.objects.filter(order=order).aggregate(
                total=Sum('quantity_ordered')
            )['total'] or 0
            
            writer.writerow([
                order.id,
                order.supplier.name,
                order.status,
                order.order_date.strftime('%Y-%m-%d %H:%M:%S'),
                order.expected_delivery.strftime('%Y-%m-%d') if order.expected_delivery else '',
                items_count,
                total_items
            ])
        
        return response
    
    elif format_type == EXCEL_EXPORT:
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        
        # Add header row
        headers = ['Order ID', 'Supplier', 'Status', 'Order Date', 
                  'Expected Delivery', 'Items Count', 'Total Items']
        
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
            total_items = OrderItem.objects.filter(order=order).aggregate(
                total=Sum('quantity_ordered')
            )['total'] or 0
            
            worksheet.write(row_num, 0, order.id)
            worksheet.write(row_num, 1, order.supplier.name)
            worksheet.write(row_num, 2, order.status)
            worksheet.write(row_num, 3, order.order_date.strftime('%Y-%m-%d %H:%M:%S'))
            
            if order.expected_delivery:
                worksheet.write(row_num, 4, order.expected_delivery.strftime('%Y-%m-%d'))
            else:
                worksheet.write(row_num, 4, '')
            
            worksheet.write(row_num, 5, items_count)
            worksheet.write(row_num, 6, total_items)
            
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
        response['Content-Disposition'] = f'attachment; filename="order_report_{start_date}_{end_date}.xlsx"'
        
        return response
    
    # Default to CSV if format not recognized
    return export_order_report(start_date, end_date, CSV_EXPORT)


def get_supplier_performance_stats(supplier_id=None, period_start=None, period_end=None):
    """
    Calculate performance statistics for suppliers.
    
    Args:
        supplier_id (int, optional): Filter by specific supplier ID. Defaults to None.
        period_start (date, optional): Start date for period. Defaults to None.
        period_end (date, optional): End date for period. Defaults to None.
    
    Returns:
        list: List of dictionaries containing supplier performance data.
    """
    # Set default period if not specified
    if not period_start:
        period_start = timezone.now().date() - datetime.timedelta(days=90)
    if not period_end:
        period_end = timezone.now().date()
    
    # Get suppliers
    suppliers_query = Supplier.objects.all()
    if supplier_id:
        suppliers_query = suppliers_query.filter(id=supplier_id)
    
    suppliers = suppliers_query.annotate(
        total_orders=Count(
            'order',
            filter=Q(
                order__order_date__date__gte=period_start,
                order__order_date__date__lte=period_end
            )
        ),
        delivered_orders=Count(
            'order',
            filter=Q(
                order__status='delivered',
                order__order_date__date__gte=period_start,
                order__order_date__date__lte=period_end
            )
        ),
        on_time_deliveries=Count(
            'order',
            filter=Q(
                order__status='delivered',
                order__order_date__date__gte=period_start,
                order__order_date__date__lte=period_end,
                order__expected_delivery__gte=F('order__order_date__date')
            )
        )
    )
    
    performance_stats = []
    
    for supplier in suppliers:
        on_time_percentage = 0
        if supplier.delivered_orders > 0:
            on_time_percentage = (supplier.on_time_deliveries / supplier.delivered_orders) * 100
        
        performance_stats.append({
            'supplier': supplier,
            'total_orders': supplier.total_orders,
            'delivered_orders': supplier.delivered_orders,
            'on_time_deliveries': supplier.on_time_deliveries,
            'on_time_percentage': on_time_percentage,
            'period_start': period_start,
            'period_end': period_end,
        })
    
    return performance_stats