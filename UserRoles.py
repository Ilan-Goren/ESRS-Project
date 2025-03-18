from django.db import models
from django.contrib.auth.models import Group, Permission, User
from django.contrib.contenttypes.models import ContentType

# User Roles: Extend the Django User Model
class Profile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Manager', 'Manager'),
        ('Staff', 'Staff'),
    ]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# Function to Create Groups & Assign Permissions
def create_user_groups():
    admin_group, created = Group.objects.get_or_create(name='Admin')
    manager_group, created = Group.objects.get_or_create(name='Manager')
    staff_group, created = Group.objects.get_or_create(name='Staff')
    
    # Assign Permissions to Manager
    content_type = ContentType.objects.get(app_label='your_app_name', model='inventoryitem')
    permission = Permission.objects.get(codename='change_inventoryitem', content_type=content_type)
    
    manager_group.permissions.add(permission)

# Run this function once (Do not include it inside the model)
create_user_groups()

# Inventory Model
class InventoryItem(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    quantity = models.PositiveIntegerField()
    reorder_level = models.PositiveIntegerField()  # When to trigger re-order
    expiry_date = models.DateField(null=True, blank=True)
    supplier = models.ForeignKey("Supplier", on_delete=models.SET_NULL, null=True, blank=True)

    def is_low_stock(self):
        return self.quantity <= self.reorder_level

    def is_expired(self):
        from django.utils.timezone import now
        return self.expiry_date and self.expiry_date < now().date()

    def __str__(self):
        return f"{self.name} ({self.quantity})"

class StockReport(models.Model):
    created_at = models.DataTimeField(auto_now_add=True)
    total_items = models.PositiveIntegerField()
    low_stock_items = models.PositiveIntegerField()
    expired_items = models.PositiveIntegerField()

# Supplier Model
class Supplier(models.Model):
    name = models.CharField(max_length=255)
    contact_email = models.EmailField(unique=True)
    contact_phone = models.CharField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.name

class SupplierPerformance(models.Model):
    supplier = models.ForeignKey("Supplier", on_delete=models.CASCADE)
    total_oders = models.PositiveIntegerField()
    successful_deliveries = models.POsitiveINtegerField()
    delayed_orders = models.PositiveIntegerField()
    avg_delivery_time = models.FloatField()

    def success_rate(self):
        return(self.successful_deliveries / self.total_orders) * 100 if self.total_orders > 0 else 0

# Order Model (Tracking orders placed with suppliers)
class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Delivered', 'Delivered'),
    ]
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)  # Who placed the order
    items = models.ManyToManyField(InventoryItem, through="OrderItem")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='Pending')
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order {self.id} - {self.supplier.name} - {self.status}"

# Order Items (Linking Inventory and Orders)
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    inventory_item = models.ForeignKey(InventoryItem, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.inventory_item.name} x {self.quantity}"

class OrderSummary(models.Model):
    create_at = models.DateTimeField(auto_now_add=True)
    total_orders = models.PositiveIntegerField()
    pending_orders = models.PositiveIntegerField()
    delivered_orders = models.PositiveIntegerField()


# Notification Model (Alerts for Low Stock & Expiry)
class Notification(models.Model):
    message = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return self.message

