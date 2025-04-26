# Restaurant Management System

A comprehensive web application for restaurant inventory and supplier management built with Django and MySQL.

## Overview

This system provides a complete solution for restaurant inventory management with separate interfaces for store management (admin, manager, staff) and supplier functionality. It offers inventory tracking, order management, performance analytics, and reporting capabilities.

## Features

- **Role-Based Access Control**: Different interfaces for admins, managers, staff, and suppliers
- **Inventory Management**: Track items, quantities, expiry dates, and supplier information
- **Order Processing**: Create orders, track status, and manage deliveries
- **Reporting System**: Generate reports for inventory, orders, and supplier performance
- **Dashboard Analytics**: Visual representation of key metrics and alerts
- **Supplier Portal**: Dedicated interface for suppliers to manage orders and deliveries

## System Requirements

- Python 3.8+
- MySQL 5.7+ (via XAMPP)
- Django 4.2+

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/restaurant-management.git
cd restaurant-management
```

### 2. Set Up the Database

1. Start XAMPP Control Panel and ensure MySQL service is running
2. Create a new database named `restaurant_inventory`
3. Import the database schema from `restaurant_inventory.sql`

### 3. Set Up Python Environment

```bash
# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 4. Configure Django Settings

Review and update the following in `restaurant_management/settings.py`:

- Database connection settings
- Secret key (for production)
- Debug settings (disable for production)

### 5. Run Migrations

```bash
python manage.py migrate
```

### 6. Create Initial Admin User

```bash
python manage.py createsuperuser
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

The application will be available at http://127.0.0.1:8000/

## Project Structure

```
restaurant_management/
│
├── manage.py
├── restaurant_management/       # Main project settings
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── utils/                  # Shared utility functions
│
├── store/                      # Store management app
│   ├── models.py               # Database models
│   ├── views.py                # View functions
│   ├── forms.py                # Form definitions
│   ├── admin.py                # Admin site configuration
│   ├── urls.py                 # URL routing
│   ├── reports.py              # Report generation
│   └── templates/              # HTML templates
│
└── supplier/                   # Supplier portal app
    ├── models.py
    ├── views.py
    ├── forms.py
    ├── urls.py
    └── templates/
```

## User Roles

### Admin
- Full access to all features
- Manage users and system settings
- View all reports and analytics

### Manager
- Manage inventory and orders
- Generate reports
- Monitor performance metrics

### Staff
- View inventory levels
- Record item usage
- Place new orders

### Supplier
- View and manage orders
- Update delivery status
- Access performance metrics

## Database Schema

The application uses the schema defined in `restaurant_inventory.sql`, which includes tables for:

- `users`: User accounts with role information
- `inventory`: Inventory items with quantities and supplier references
- `suppliers`: Supplier information
- `orders`: Order header information
- `order_items`: Individual items within orders
- `transactions`: Record of inventory changes

## Maintenance Tasks

### Update Supplier Performance Metrics

```bash
python manage.py update_supplier_performance --months=3
```

### Clean Up Expired Inventory

```bash
python manage.py cleanup_expired --days=7 --remove
```

## Deployment Considerations

For production deployment:

1. Set `DEBUG = False` in settings.py
2. Configure a proper production database
3. Set up proper static file serving
4. Use a production-ready web server (Gunicorn, uWSGI)
5. Configure HTTPS with a valid SSL certificate

## License

[MIT License](LICENSE)

## Contributors

- Your Name <your.email@example.com>