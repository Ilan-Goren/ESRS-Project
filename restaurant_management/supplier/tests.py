"""
Tests for the supplier application.

This module contains test cases for models, views, forms, and other components
of the supplier application.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
import datetime

from store.models import UserProfile, Supplier, Order
from .models import SupplierProfile, DeliveryNotification, SupplierPerformance


class SupplierProfileModelTests(TestCase):
    """Test cases for the SupplierProfile model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='supplier',
            email='supplier@example.com',
            password='supplierpassword'
        )
        
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            role='supplier'
        )
        
        self.supplier = Supplier.objects.create(
            name='Test Supplier',
            email='contact@test-supplier.com',
            phone='1234567890'
        )
        
        self.supplier_profile = SupplierProfile.objects.create(
            user=self.user,
            supplier=self.supplier
        )
    
    def test_supplier_profile_creation(self):
        """Test that a supplier profile can be created."""
        self.assertEqual(self.supplier_profile.user.username, 'supplier')
        self.assertEqual(self.supplier_profile.supplier.name, 'Test Supplier')
    
    def test_supplier_profile_string_representation(self):
        """Test the string representation of a supplier profile."""
        expected_string = f"Supplier Profile: supplier - Test Supplier"
        self.assertEqual(str(self.supplier_profile), expected_string)


class DeliveryNotificationModelTests(TestCase):
    """Test cases for the DeliveryNotification model."""
    
    def setUp(self):
        """Set up test data."""
        self.supplier = Supplier.objects.create(
            name='Test Supplier',
            email='contact@test-supplier.com',
            phone='1234567890'
        )
        
        self.order = Order.objects.create(
            supplier=self.supplier,
            status='shipped',
            expected_delivery=timezone.now().date() + timezone.timedelta(days=3)
        )
        
        self.notification = DeliveryNotification.objects.create(
            order=self.order,
            message='Your order will be delivered soon.',
            delivery_date=timezone.now().date() + timezone.timedelta(days=2)
        )
    
    def test_notification_creation(self):
        """Test that a delivery notification can be created."""
        self.assertEqual(self.notification.order, self.order)
        self.assertEqual(self.notification.message, 'Your order will be delivered soon.')
    
    def test_notification_string_representation(self):
        """Test the string representation of a delivery notification."""
        expected_string = f"Delivery notification for Order #{self.order.id}"
        self.assertEqual(str(self.notification), expected_string)


class SupplierPerformanceModelTests(TestCase):
    """Test cases for the SupplierPerformance model."""
    
    def setUp(self):
        """Set up test data."""
        self.supplier = Supplier.objects.create(
            name='Test Supplier',
            email='contact@test-supplier.com',
            phone='1234567890'
        )
        
        self.today = timezone.now().date()
        self.month_start = self.today.replace(day=1)
        self.month_end = (self.month_start + datetime.timedelta(days=32)).replace(day=1) - datetime.timedelta(days=1)
        
        self.performance = SupplierPerformance.objects.create(
            supplier=self.supplier,
            total_orders=10,
            on_time_deliveries=8,
            late_deliveries=2,
            quality_rating=4.5,
            period_start=self.month_start,
            period_end=self.month_end
        )
    
    def test_performance_creation(self):
        """Test that a supplier performance record can be created."""
        self.assertEqual(self.performance.supplier, self.supplier)
        self.assertEqual(self.performance.total_orders, 10)
        self.assertEqual(self.performance.on_time_deliveries, 8)
    
    def test_on_time_percentage(self):
        """Test the on_time_percentage property."""
        self.assertEqual(self.performance.on_time_percentage, 80.0)
        
        # Test with zero orders
        zero_performance = SupplierPerformance.objects.create(
            supplier=self.supplier,
            total_orders=0,
            on_time_deliveries=0,
            late_deliveries=0,
            quality_rating=0.0,
            period_start=self.month_start - datetime.timedelta(days=32),
            period_end=self.month_end - datetime.timedelta(days=32)
        )
        self.assertEqual(zero_performance.on_time_percentage, 0)


class SupplierViewTests(TestCase):
    """Test cases for supplier views."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        
        # Create supplier user
        self.user = User.objects.create_user(
            username='supplier',
            email='supplier@example.com',
            password='supplierpassword'
        )
        
        self.user_profile = UserProfile.objects.create(
            user=self.user,
            role='supplier'
        )
        
        self.supplier = Supplier.objects.create(
            name='Test Supplier',
            email='contact@test-supplier.com',
            phone='1234567890'
        )
        
        self.supplier_profile = SupplierProfile.objects.create(
            user=self.user,
            supplier=self.supplier
        )
        
        # Create some orders
        self.order1 = Order.objects.create(
            supplier=self.supplier,
            status='pending',
            order_date=timezone.now() - datetime.timedelta(days=2),
            expected_delivery=timezone.now().date() + datetime.timedelta(days=3)
        )
        
        self.order2 = Order.objects.create(
            supplier=self.supplier,
            status='shipped',
            order_date=timezone.now() - datetime.timedelta(days=5),
            expected_delivery=timezone.now().date() + datetime.timedelta(days=1)
        )
        
        self.order3 = Order.objects.create(
            supplier=self.supplier,
            status='delivered',
            order_date=timezone.now() - datetime.timedelta(days=10),
            expected_delivery=timezone.now().date() - datetime.timedelta(days=3)
        )
    
    def test_login_required(self):
        """Test that login is required for supplier views."""
        response = self.client.get(reverse('supplier:dashboard'))
        self.assertNotEqual(response.status_code, 200)  # Should redirect to login
    
    def test_supplier_dashboard(self):
        """Test the supplier dashboard view."""
        self.client.login(username='supplier', password='supplierpassword')
        response = self.client.get(reverse('supplier:dashboard'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Supplier')
        
        # Check context data
        self.assertEqual(response.context['pending_orders'], 1)
        self.assertEqual(response.context['shipped_orders'], 1)
        self.assertEqual(response.context['delivered_orders'], 1)
    
    def test_order_details(self):
        """Test the order details view."""
        self.client.login(username='supplier', password='supplierpassword')
        response = self.client.get(reverse('supplier:order_details', args=[self.order1.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, f'Order #{self.order1.id}')
    
    def test_update_delivery_status(self):
        """Test the update delivery status view."""
        self.client.login(username='supplier', password='supplierpassword')
        response = self.client.get(reverse('supplier:update_delivery_status', args=[self.order1.id]))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Update Delivery Status')