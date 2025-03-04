# Inventory Management System

## Overview
This is a comprehensive inventory management system frontend built with React, TypeScript, and Tailwind CSS. The system is designed to help restaurants and retail stores manage their inventory, track suppliers, handle orders, and generate reports.

## Features

- **Role-based access control**: Different interfaces for admin, manager, staff, and supplier roles  
- **Inventory management**: Track stock levels, set reorder points, and monitor expiry dates  
- **Supplier management**: Maintain supplier information and performance metrics  
- **Order processing**: Create, track, and manage purchase orders  
- **Reporting**: Generate and export inventory and order reports  

## Tech Stack

- **Frontend**: React with TypeScript  
- **Styling**: Tailwind CSS  
- **State Management**: React Context API  
- **Data Fetching**: Axios  
- **Form Handling**: React Hook Form  
- **Routing**: React Router  
- **API**: Temporary PHP API during development, will connect to Django backend later  
- **Database**: MySQL (via XAMPP)  

---

## Setup Instructions

### Prerequisites

Ensure the following are installed on your system:

- **Node.js** (v14 or later)  
- **XAMPP** (for MySQL database)  
- **Git**
- **Tailwind v3**

### Installation

#### Clone the repository:
```
git clone https://github.com/yourusername/inventory-system.git
cd inventory-system
```

#### Install dependencies:
```
npm install
```

#### Set up the PHP API:
- Copy the PHP files to your XAMPP `htdocs` directory.  
- Import the MySQL database schema using phpMyAdmin.

#### Start the development server:
```
npm run dev
```

- Open your browser and navigate to **[http://localhost:5173](http://localhost:5173)**

---

## Project Structure

```
/src/components
  ├── /common      # Common UI elements (buttons, cards, etc.)
  ├── /forms       # Form components
  ├── /layout      # Layout components (header, sidebar, etc.)
  ├── /tables      # Table and data display components

/src/context      # React contexts (auth, etc.)
/src/hooks        # Custom React hooks
/src/pages        # Page components for different routes and user roles
/src/services     # API service functions
/src/utils        # Utility functions
```

---

## User Authentication

The system supports multiple user roles:

- **Admin**: Full system access, including user management  
- **Manager**: Inventory management, supplier relationships, reporting  
- **Staff**: Daily inventory operations, order creation  
- **Supplier**: Order fulfillment and delivery updates  

### Test Accounts

| Role     | Email                 | Password (Hashed) |
|----------|-----------------------|-------------------|
| Admin    | admin@example.com     | hashedpassword1  |
| Manager  | manager@example.com   | hashedpassword2  |
| Staff    | staff@example.com     | hashedpassword3  |
| Supplier | supplier@example.com  | hashedpassword4  |

---

## Database Structure

The MySQL database includes the following tables:

- **users**: User accounts and roles  
- **inventory**: Inventory items with quantities and attributes  
- **suppliers**: Supplier contact information  
- **orders**: Purchase orders  
- **order_items**: Items within purchase orders  
- **transactions**: Record of inventory movements  

---

## API Endpoints

The temporary PHP API includes endpoints for:

- **Authentication**: `/auth.php`  
- **Inventory management**: `/inventory.php`  
- **Supplier management**: `/suppliers.php`  
- **Order management**: `/orders.php`  

---

## Future Integration with Django Backend

The frontend is designed to easily transition from the temporary PHP API to a **Django REST API**:

- **Update the API URL** in `src/services/api.ts`.  
- **Adjust authentication methods** to match Django's JWT or token-based auth.  
- **Update service functions** to align with Django's API endpoints and response formats.  

---
