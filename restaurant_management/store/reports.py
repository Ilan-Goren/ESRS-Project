"""
Reporting module for the store application.

This module contains functions for generating various reports for inventory,
orders, transactions, and suppliers.
"""

import csv
import io
import datetime
from django.db.models import Sum, Count, Q, F, Avg
from django.utils import timezone
from django.http import HttpResponse
from django.template.loader import render_to_string

import xlsxwriter
from io import BytesIO

from .models import Inventory, Order, OrderItem, Transaction, Supplier
from restaurant_management.utils.constants import (
    CSV_EXPORT, EXCEL_EXPORT, PDF_EXPORT,
    STOCK_REPORT, ORDER_REPORT, SUPPLIER_REPORT, TRANSACTION_REPORT
)


class ReportGenerator:
    """Base class for report generators."""
    
    def __init__(self, start_date=None, end_date=None, format_type=CSV_EXPORT):
        """
        Initialize the report generator.
        
        Args:
            start_date (date, optional): Start date for report period. Defaults to None.
            end_date (date, optional): End date for report period. Defaults to None.
            format_type (str, optional): Export format. Defaults to CSV_EXPORT.
        """
        # Set default dates if not provided
        if not start_date:
            self.start_date = timezone.now().date() - datetime.timedelta(days=30)
        else:
            self.start_date = start_date
        
        if not end_date:
            self.end_date = timezone.now().date()
        else:
            self.end_date = end_date
        
        self.format_type = format_type
    
    def generate(self):
        """
        Generate the report.
        
        This method should be implemented by subclasses.
        
        Returns:
            HttpResponse: The report as an HTTP response.
        """
        raise NotImplementedError("Subclasses must implement this method.")
    
    def _generate_csv(self, filename, headers, data):
        """
        Generate a CSV report.
        
        Args:
            filename (str): Name of the file.
            headers (list): List of column headers.
            data (list): List of data rows.
        
        Returns:
            HttpResponse: The CSV report as an HTTP response.
        """
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
        
        writer = csv.writer(response)
        writer.writerow(headers)
        
        for row in data:
            writer.writerow(row)
        
        return response
    
    def _generate_excel(self, filename, headers, data):
        """
        Generate an Excel report.
        
        Args:
            filename (str): Name of the file.
            headers (list): List of column headers.
            data (list): List of data rows.
        
        Returns:
            HttpResponse: The Excel report as an HTTP response.
        """
        output = BytesIO()
        workbook = xlsxwriter.Workbook(output)
        worksheet = workbook.add_worksheet()
        
        # Add header row with formatting
        header_format = workbook.add_format({
            'bold': True,
            'bg_color': '#f0f0f0',
            'border': 1
        })
        
        for col_num, header in enumerate(headers):
            worksheet.write(0, col_num, header, header_format)
        
        # Add data rows
        for row_num, row_data in enumerate(data, 1):
            for col_num, cell_value in enumerate(row_data):
                worksheet.write(row_num, col_num, cell_value)
        
        # Adjust column widths
        for col_num, header in enumerate(headers):
            worksheet.set_column(col_num, col_num, len(header) + 5)
        
        workbook.close()
        output.seek(0)
        
        response = HttpResponse(
            output.read(),
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
        response['Content-Disposition'] = f'attachment; filename="{filename}.xlsx"'
        
        return response


class InventoryReportGenerator(ReportGenerator):
    """Generator for inventory reports."""
    
    def generate(self):
        """
        Generate an inventory report.
        
        Returns:
            HttpResponse: The inventory report as an HTTP response.
        """
        inventory_items = Inventory.objects.select_related('supplier').all()
        
        headers = [
            'ID', 'SKU', 'Item Name', 'Category', 'Quantity', 
            'Reorder Level', 'Expiry Date', 'Supplier', 'Low Stock', 'Last Updated'
        ]
        
        data = []
        for item in inventory_items:
            row = [
                item.id,
                item.sku or '',
                item.item_name,
                item.category or '',
                item.quantity,
                item.reorder_level,
                item.expiry_date.strftime('%Y-%m-%d') if item.expiry_date else '',
                item.supplier.name if item.supplier else '',
                'Yes' if item.is_low_stock else 'No',
                item.last_updated.strftime('%Y-%m-%d %H:%M')
            ]
            data.append(row)
        
        if self.format_type == CSV_EXPORT:
            return self._generate_csv('inventory_report', headers, data)
        elif self.format_type == EXCEL_EXPORT:
            return self._generate_excel('inventory_report', headers, data)
        else:
            # Default to CSV if format not supported
            return self._generate_csv('inventory_report', headers, data)


class OrderReportGenerator(ReportGenerator):
    """Generator for order reports."""
    
    def generate(self):
        """
        Generate an order report.
        
        Returns:
            HttpResponse: The order report as an HTTP response.
        """
        orders = Order.objects.filter(
            order_date__date__gte=self.start_date,
            order_date__date__lte=self.end_date
        ).select_related('supplier')
        
        headers = [
            'Order ID', 'Supplier', 'Status', 'Order Date', 
            'Expected Delivery', 'Items Count', 'Total Quantity'
        ]
        
        data = []
        for order in orders:
            items_count = OrderItem.objects.filter(order=order).count()
            total_quantity = OrderItem.objects.filter(order=order).aggregate(
                total=Sum('quantity_ordered')
            )['total'] or 0
            
            row = [
                order.id,
                order.supplier.name,
                order.status,
                order.order_date.strftime('%Y-%m-%d %H:%M'),
                order.expected_delivery.strftime('%Y-%m-%d') if order.expected_delivery else 'Not specified',
                items_count,
                total_quantity
            ]
            data.append(row)
        
        if self.format_type == CSV_EXPORT:
            return self._generate_csv(f'order_report_{self.start_date}_to_{self.end_date}', headers, data)
        elif self.format_type == EXCEL_EXPORT:
            return self._generate_excel(f'order_report_{self.start_date}_to_{self.end_date}', headers, data)
        else:
            # Default to CSV if format not supported
            return self._generate_csv(f'order_report_{self.start_date}_to_{self.end_date}', headers, data)


class TransactionReportGenerator(ReportGenerator):
    """Generator for transaction reports."""
    
    def generate(self):
        """
        Generate a transaction report.
        
        Returns:
            HttpResponse: The transaction report as an HTTP response.
        """
        transactions = Transaction.objects.filter(
            created_at__date__gte=self.start_date,
            created_at__date__lte=self.end_date
        ).select_related('inventory', 'user__user')
        
        headers = [
            'Transaction ID', 'Item', 'Category', 'User', 'Type', 
            'Quantity', 'Date/Time'
        ]
        
        data = []
        for transaction in transactions:
            row = [
                transaction.id,
                transaction.inventory.item_name,
                transaction.inventory.category or 'N/A',
                transaction.user.user.username,
                transaction.transaction_type,
                transaction.quantity_used,
                transaction.created_at.strftime('%Y-%m-%d %H:%M')
            ]
            data.append(row)
        
        if self.format_type == CSV_EXPORT:
            return self._generate_csv(f'transaction_report_{self.start_date}_to_{self.end_date}', headers, data)
        elif self.format_type == EXCEL_EXPORT:
            return self._generate_excel(f'transaction_report_{self.start_date}_to_{self.end_date}', headers, data)
        else:
            # Default to CSV if format not supported
            return self._generate_csv(f'transaction_report_{self.start_date}_to_{self.end_date}', headers, data)


class SupplierReportGenerator(ReportGenerator):
    """Generator for supplier performance reports."""
    
    def generate(self):
        """
        Generate a supplier performance report.
        
        Returns:
            HttpResponse: The supplier report as an HTTP response.
        """
        suppliers = Supplier.objects.all()
        
        headers = [
            'Supplier ID', 'Supplier Name', 'Total Orders', 'Delivered Orders',
            'On-Time Deliveries', 'Late Deliveries', 'On-Time %', 'Average Delivery Time (days)'
        ]
        
        data = []
        for supplier in suppliers:
            # Get orders for this supplier in the date range
            orders = Order.objects.filter(
                supplier=supplier,
                order_date__date__gte=self.start_date,
                order_date__date__lte=self.end_date
            )
            
            total_orders = orders.count()
            
            # Skip if no orders in this period
            if total_orders == 0:
                continue
            
            delivered_orders = orders.filter(status='delivered').count()
            
            # Calculate on-time deliveries
            on_time_deliveries = 0
            late_deliveries = 0
            total_delivery_days = 0
            
            for order in orders.filter(status='delivered'):
                # Check if expected_delivery is set
                if order.expected_delivery:
                    # Check if there's a delivery notification
                    try:
                        from supplier.models import DeliveryNotification
                        notification = DeliveryNotification.objects.get(order=order)
                        delivery_date = notification.delivery_date
                        
                        # Calculate delivery time
                        delivery_time = (delivery_date - order.order_date.date()).days
                        total_delivery_days += delivery_time
                        
                        if delivery_date <= order.expected_delivery:
                            on_time_deliveries += 1
                        else:
                            late_deliveries += 1
                            
                    except Exception:
                        # If no delivery notification, use order status update time
                        on_time_deliveries += 1  # Assume on time if we can't tell
                else:
                    on_time_deliveries += 1  # Assume on time if no expected delivery date
            
            # Calculate on-time percentage
            if delivered_orders > 0:
                on_time_percentage = (on_time_deliveries / delivered_orders) * 100
                avg_delivery_time = total_delivery_days / delivered_orders if total_delivery_days > 0 else 'N/A'
            else:
                on_time_percentage = 'N/A'
                avg_delivery_time = 'N/A'
            
            row = [
                supplier.id,
                supplier.name,
                total_orders,
                delivered_orders,
                on_time_deliveries,
                late_deliveries,
                f"{on_time_percentage:.1f}%" if isinstance(on_time_percentage, float) else on_time_percentage,
                f"{avg_delivery_time:.1f}" if isinstance(avg_delivery_time, float) else avg_delivery_time
            ]
            data.append(row)
        
        if self.format_type == CSV_EXPORT:
            return self._generate_csv(f'supplier_report_{self.start_date}_to_{self.end_date}', headers, data)
        elif self.format_type == EXCEL_EXPORT:
            return self._generate_excel(f'supplier_report_{self.start_date}_to_{self.end_date}', headers, data)
        else:
            # Default to CSV if format not supported
            return self._generate_csv(f'supplier_report_{self.start_date}_to_{self.end_date}', headers, data)


def get_report_generator(report_type, start_date=None, end_date=None, format_type=CSV_EXPORT):
    """
    Factory function to get the appropriate report generator.
    
    Args:
        report_type (str): Type of report to generate.
        start_date (date, optional): Start date for report period. Defaults to None.
        end_date (date, optional): End date for report period. Defaults to None.
        format_type (str, optional): Export format. Defaults to CSV_EXPORT.
    
    Returns:
        ReportGenerator: The appropriate report generator instance.
    
    Raises:
        ValueError: If the report type is not recognized.
    """
    if report_type == STOCK_REPORT:
        return InventoryReportGenerator(start_date, end_date, format_type)
    elif report_type == ORDER_REPORT:
        return OrderReportGenerator(start_date, end_date, format_type)
    elif report_type == TRANSACTION_REPORT:
        return TransactionReportGenerator(start_date, end_date, format_type)
    elif report_type == SUPPLIER_REPORT:
        return SupplierReportGenerator(start_date, end_date, format_type)
    else:
        raise ValueError(f"Unrecognized report type: {report_type}")