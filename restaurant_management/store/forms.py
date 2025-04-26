"""
Forms for the store application.

These forms handle user input for authentication, inventory management,
order processing, and other store-related functionality.
"""

from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from .models import Inventory, Supplier, Order, OrderItem, Transaction, UserProfile


class CustomAuthenticationForm(AuthenticationForm):
    """
    Custom authentication form with enhanced styling and validation.
    """
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
    )


class UserRegistrationForm(UserCreationForm):
    """
    Form for registering new users with role selection.
    """
    USER_ROLES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
        ('supplier', 'Supplier'),
    )
    
    role = forms.ChoiceField(
        choices=USER_ROLES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=True
    )
    
    supplier = forms.ModelChoiceField(
        queryset=Supplier.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        required=True
    )
    
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'role', 'supplier')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(UserRegistrationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Confirm Password'})
    
    def clean(self):
        cleaned_data = super().clean()
        role = cleaned_data.get('role')
        supplier = cleaned_data.get('supplier')
        
        if role == 'supplier' and not supplier:
            raise ValidationError(_("A supplier must be selected for users with the 'supplier' role."))
        
        return cleaned_data


class InventoryForm(forms.ModelForm):
    """
    Form for adding or editing inventory items.
    """
    class Meta:
        model = Inventory
        fields = ('sku', 'item_name', 'category', 'quantity', 'reorder_level', 'expiry_date', 'supplier')
        widgets = {
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'item_name': forms.TextInput(attrs={'class': 'form-control'}),
            'category': forms.TextInput(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control'}),
            'expiry_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'supplier': forms.Select(attrs={'class': 'form-control'}),
        }


class TransactionForm(forms.ModelForm):
    """
    Form for recording inventory transactions (additions, removals, adjustments).
    """
    class Meta:
        model = Transaction
        fields = ('inventory', 'quantity_used', 'transaction_type')
        widgets = {
            'inventory': forms.Select(attrs={'class': 'form-control'}),
            'quantity_used': forms.NumberInput(attrs={'class': 'form-control'}),
            'transaction_type': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_quantity_used(self):
        quantity = self.cleaned_data.get('quantity_used')
        if quantity <= 0:
            raise ValidationError(_("Quantity must be greater than zero."))
        return quantity


class OrderForm(forms.ModelForm):
    """
    Form for creating new orders.
    """
    class Meta:
        model = Order
        fields = ('supplier', 'expected_delivery')
        widgets = {
            'supplier': forms.Select(attrs={'class': 'form-control'}),
            'expected_delivery': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class OrderItemForm(forms.ModelForm):
    """
    Form for adding items to an order.
    """
    class Meta:
        model = OrderItem
        fields = ('inventory', 'quantity_ordered')
        widgets = {
            'inventory': forms.Select(attrs={'class': 'form-control'}),
            'quantity_ordered': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
    def clean_quantity_ordered(self):
        quantity = self.cleaned_data.get('quantity_ordered')
        if quantity <= 0:
            raise ValidationError(_("Quantity must be greater than zero."))
        return quantity


class OrderUpdateForm(forms.ModelForm):
    """
    Form for updating order status.
    """
    class Meta:
        model = Order
        fields = ('status',)
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }


class DateRangeForm(forms.Form):
    """
    Form for selecting date ranges for reports.
    """
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=True
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=True
    )
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise ValidationError(_("End date must be after start date."))
        
        return cleaned_data


class UserProfileForm(forms.ModelForm):
    """
    Form for updating user profiles.
    """
    class Meta:
        model = UserProfile
        fields = ('role',)
        widgets = {
            'role': forms.Select(attrs={'class': 'form-control'}),
        }