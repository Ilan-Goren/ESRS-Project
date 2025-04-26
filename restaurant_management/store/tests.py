"""
Tests for the store application.

This module contains test cases for models, views, forms, and other components
of the store application.
"""

from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone

from .models import UserProfile, Inventory, Supplier, Order, OrderItem, Transaction


class UserProfileModelTests(TestCase):
    """Test cases for the UserProfile model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        
        self.profile = UserProfile.objects.create(
            user=self.user,
            role='admin'
        )
    
    def test_profile_creation(self):
        """Test that a profile can be created."""
        self.assertEqual(self.profile.user.username, 'testuser')
        self.assertEqual(self.profile.role, 'admin')
    
    def test_role_properties(self):
        """Test that role properties work correctly."""
        self.assertTrue(self.profile.is_admin)
        self.assertFalse(self.profile.is_manager)
        self.assertFalse(self.profile.is_staff)
        self.assertFalse(self.profile.is_supplier)
        
        # Change role and test again
        self.profile.role = 'manager'
        self.profile.save()
        
        self.assertFalse(self.profile.is_admin)
        self.assertTrue(self.profile.is_manager)
        self.assertFalse(self.profile.is_staff)
        self.assertFalse(self.profile.is_supplier)


class InventoryModelTests(TestCase):
    """Test cases for the Inventory model."""
    
    def setUp(self):
        """Set up test data."""
        self.supplier = Supplier.objects.create(
            name='Test Supplier',
            email='supplier@example.com',
            phone='1234567890'
        )
        
        self.inventory = Inventory.objects.create(
            item_name='Test Item',
            category='Test Category',
            quantity=50,
            reorder_level=10,
            expiry_date=timezone.now().date() + timezone.timedelta(days=30),
            supplier=self.supplier
        )
    
    def test_inventory_creation(self):
        """Test that an inventory item can be created."""
        self.assertEqual(self.inventory.item_name, 'Test Item')
        self.assertEqual(self.inventory.quantity, 50)
        self.assertEqual(self.inventory.supplier, self.supplier)
    
    def test_inventory_methods(self):
        """Test inventory methods."""
        # Test is_low_stock when above reorder level
        self.assertFalse(self.inventory.is_low_stock)
        
        # Test is_low_stock when at reorder level
        self.inventory.quantity = 10
        self.inventory.save()
        self.assertTrue(self.inventory.is_low_stock)
        
        # Test is_low_stock when below reorder level
        self.inventory.quantity = 5
        self.inventory.save()
        self.assertTrue(self.inventory.is_low_stock)
        
        # Test is_expired when not expired
        self.assertFalse(self.inventory.is_expired)
        
        # Test is_expired when expired
        self.inventory.expiry_date = timezone.now().date() - timezone.timedelta(days=1)
        self.inventory.save()
        self.assertTrue(self.inventory.is_expired)


class AuthenticationTests(TestCase):
    """Test cases for authentication functionality."""
    
    def setUp(self):
        """Set up test data."""
        self.client = Client()
        
        # Create users with different roles
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpassword'
        )
        UserProfile.objects.create(
            user=self.admin_user,
            role='admin'
        )
        
        self.staff_user = User.objects.create_user(
            username='staff',
            email='staff@example.com',
            password='staffpassword'
        )
        UserProfile.objects.create(
            user=self.staff_user,
            role='staff'
        )
        
        self.supplier_user = User.objects.create_user(
            username='supplier',
            email='supplier@example.com',
            password='supplierpassword'
        )
        UserProfile.objects.create(
            user=self.supplier_user,
            role='supplier'
        )
    
    def test_login_redirects(self):
        """Test that login redirects to the appropriate dashboard."""
        # Test admin login
        response = self.client.post(reverse('login'), {
            'username': 'admin',
            'password': 'adminpassword'
        }, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('landing_page'))
        
        # Test staff login
        self.client.logout()
        response = self.client.post(reverse('login'), {
            'username': 'staff',
            'password': 'staffpassword'
        }, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('landing_page'))
        
        # Test supplier login
        self.client.logout()
        response = self.client.post(reverse('login'), {
            'username': 'supplier',
            'password': 'supplierpassword'
        }, follow=True)
        
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('landing_page'))
    
    def test_role_based_access(self):
        """Test that users can only access appropriate pages based on role."""
        # Test admin access
        self.client.login(username='admin', password='adminpassword')
        response = self.client.get(reverse('store:admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Test staff access restriction
        self.client.login(username='staff', password='staffpassword')
        response = self.client.get(reverse('store:admin_dashboard'))
        self.assertNotEqual(response.status_code, 200)  # Should not be accessible
        
        # Test supplier access restriction
        self.client.login(username='supplier', password='supplierpassword')
        response = self.client.get(reverse('store:staff_dashboard'))
        self.assertNotEqual(response.status_code, 200)  # Should not be accessible