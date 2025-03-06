from django.db import models
from django.contrib.auth.models import User


# Models: Admin, Manager, Staff (use AbstractUser)

class Supplier(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    company_name = models.CharField(max_length=255)
    contact_email = models.EmailField(unique=True)
    contact_phone = models.ChaField(max_length=15)
    address = models.TextField()

    def __str__(self):
        return self.company_name
    
class Product(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, relate_name="products")
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock_quantity = models.PositiveIntegerField()
    is_avaliable = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.suppliers.company_name}"
    
class Order (models.Model):
    supplier = models.ForeignKey(Supplier, on_delete=models.CASCADE, related_name="orders")
    customer_name = models.CharField(max_length=255)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_palces= 2)
    status_choices = [('Pending', 'Pending'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')]
    status = models.CharField(max_length=20, choices=status_choices, defaults='Pending')

    def __str__(self):
        return f"Order {self.id} - {self.customer_name} - {self.status}"
    
class Delivery(models.Models):
    order = models.OneToOneField(Order, on_deleted=models.CASCADE, related_name="delivery")
    delivery_date = models.DateField()
    is_delivery = models.BooleanField(default=False)

    def __str__(self):
        return f"Delivery for Order {self.order.id} - {'Delivery' if self.is_delivery else 'Pending'}"
    
class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name="payment")
    payment_status_choices = [('Pending', 'Pending'), ('Paid', 'Paid')]
    status = models.CharField(max_length=10, choices=payment_status_choices, default='Pending')
    payment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PAyment for order {self.order.id} - {self.status}"
    

    