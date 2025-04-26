"""
Forms for the supplier application.

These forms handle supplier-specific functionality, such as updating order statuses,
confirming deliveries, and managing supplier profiles.
"""

from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from store.models import Order, Supplier
from .models import DeliveryNotification


class SupplierLoginForm(forms.Form):
    """
    Custom login form for suppliers.
    """
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        required=True
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}),
        required=True
    )


class OrderStatusUpdateForm(forms.ModelForm):
    """
    Form for suppliers to update order status.
    """
    class Meta:
        model = Order
        fields = ('status',)
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super(OrderStatusUpdateForm, self).__init__(*args, **kwargs)
        # Limit the status choices for suppliers
        self.fields['status'].choices = [
            ('pending', 'Pending'),
            ('shipped', 'Shipped'),
            ('delivered', 'Delivered'),
        ]
    
    def clean_status(self):
        status = self.cleaned_data.get('status')
        current_status = self.instance.status
        
        # Enforce logical status progression
        if current_status == 'pending' and status == 'delivered':
            raise ValidationError(_("Order must be shipped before it can be delivered."))
        
        if current_status == 'delivered' and status != 'delivered':
            raise ValidationError(_("Cannot change status of a delivered order."))
        
        if current_status == 'cancelled':
            raise ValidationError(_("Cannot update a cancelled order."))
        
        return status


class DeliveryNotificationForm(forms.ModelForm):
    """
    Form for creating delivery notifications.
    """
    class Meta:
        model = DeliveryNotification
        fields = ('message', 'delivery_date')
        widgets = {
            'message': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'delivery_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
    
    def clean_delivery_date(self):
        delivery_date = self.cleaned_data.get('delivery_date')
        today = timezone.now().date()
        
        if delivery_date < today:
            raise ValidationError(_("Delivery date cannot be in the past."))
        
        return delivery_date


class SupplierProfileUpdateForm(forms.ModelForm):
    """
    Form for updating supplier profile information.
    """
    class Meta:
        model = Supplier
        fields = ('name', 'contact_info', 'email', 'phone')
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'contact_info': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
        }


class OrderSearchForm(forms.Form):
    """
    Form for searching orders by date range and status.
    """
    STATUS_CHOICES = (
        ('', 'All'),
        ('pending', 'Pending'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    )
    
    start_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False
    )
    end_date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        required=False
    )
    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'}),
        required=False
    )
    
    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get('start_date')
        end_date = cleaned_data.get('end_date')
        
        if start_date and end_date and start_date > end_date:
            raise ValidationError(_("End date must be after start date."))
        
        return cleaned_data