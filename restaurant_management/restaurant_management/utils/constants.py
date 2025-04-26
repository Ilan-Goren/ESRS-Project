"""
Constants used throughout the restaurant management system.

This module contains application-wide constants to maintain consistency across
the codebase and make it easier to modify system-wide configuration values.
"""

# User roles
ADMIN_ROLE = 'admin'
MANAGER_ROLE = 'manager'
STAFF_ROLE = 'staff'
SUPPLIER_ROLE = 'supplier'

USER_ROLE_CHOICES = (
    (ADMIN_ROLE, 'Admin'),
    (MANAGER_ROLE, 'Manager'),
    (STAFF_ROLE, 'Staff'),
    (SUPPLIER_ROLE, 'Supplier'),
)

# Order statuses
PENDING_STATUS = 'pending'
SHIPPED_STATUS = 'shipped'
DELIVERED_STATUS = 'delivered'
CANCELLED_STATUS = 'cancelled'

ORDER_STATUS_CHOICES = (
    (PENDING_STATUS, 'Pending'),
    (SHIPPED_STATUS, 'Shipped'),
    (DELIVERED_STATUS, 'Delivered'),
    (CANCELLED_STATUS, 'Cancelled'),
)

# Transaction types
ADDED_TRANSACTION = 'added'
REMOVED_TRANSACTION = 'removed'
ADJUSTED_TRANSACTION = 'adjusted'

TRANSACTION_TYPE_CHOICES = (
    (ADDED_TRANSACTION, 'Added'),
    (REMOVED_TRANSACTION, 'Removed'),
    (ADJUSTED_TRANSACTION, 'Adjusted'),
)

# Pagination settings
ITEMS_PER_PAGE = 10

# Low stock and expiry thresholds
LOW_STOCK_WARNING_DAYS = 3  # Show alert for items that are X days away from reaching reorder level
EXPIRY_WARNING_DAYS = 30  # Show alert for items expiring within X days

# Report types
STOCK_REPORT = 'stock'
ORDER_REPORT = 'order'
SUPPLIER_REPORT = 'supplier'
TRANSACTION_REPORT = 'transaction'

REPORT_TYPE_CHOICES = (
    (STOCK_REPORT, 'Stock Report'),
    (ORDER_REPORT, 'Order Report'),
    (SUPPLIER_REPORT, 'Supplier Performance Report'),
    (TRANSACTION_REPORT, 'Transaction Report'),
)

# Export formats
PDF_EXPORT = 'pdf'
CSV_EXPORT = 'csv'
EXCEL_EXPORT = 'excel'

EXPORT_FORMAT_CHOICES = (
    (PDF_EXPORT, 'PDF'),
    (CSV_EXPORT, 'CSV'),
    (EXCEL_EXPORT, 'Excel'),
)