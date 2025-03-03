This database is designed to manage the inventory of a restaurant or store. It tracks users, inventory items, suppliers, orders, transactions, and stock usage. The database ensures scalability, data integrity, and efficient querying by using foreign keys, indexing, triggers, and stored procedures.

Tables & Their Purpose
	1.	users – Stores user accounts with different roles (admin, manager, staff, supplier).
	2.	inventory – Tracks stock levels, reorder alerts, expiry dates, and supplier information.
	3.	suppliers – Stores details of suppliers providing inventory items.
	4.	orders – Records purchase orders made to suppliers.
	5.	order_items – Links inventory items to specific orders, tracking quantities ordered.
	6.	transactions – Logs stock usage, adjustments, and updates by users.

Key Relationships
	•	inventory.supplier_id → Links to suppliers.id (each inventory item has a supplier).
	•	orders.supplier_id → Links to suppliers.id (each order is placed with a supplier).
	•	order_items.inventory_id → Links to inventory.id (tracks which items are in each order).
	•	transactions.inventory_id → Links to inventory.id (logs stock movements).
	•	transactions.user_id → Links to users.id (tracks which user performed an action).


Scalability Features
	•	Uses foreign keys to maintain relationships and ensure data integrity.
	•	Indexed key columns (id, email, inventory_id, supplier_id) for faster queries.
	•	Automated stock updates using triggers (e.g., reducing stock when an order is placed).
	•	Supports expanding inventory and multiple store locations in the future.
	•	Stored procedures help automate repetitive database tasks.


How to Import the Database
	1.	Open phpMyAdmin using XAMPP.
	2.	Create a new database named restaurant_inventory.
	3.	Click Import → Select restaurant_inventory.sql → Click Go.

This structure ensures efficient inventory tracking, automated stock management, and secure data handling.