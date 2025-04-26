"""
Views for the supplier application.

These views handle supplier-specific functionality, including viewing and managing orders,
updating delivery status, and accessing supplier performance metrics.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Count, Q, F
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.utils import timezone
from django.db import transaction

from store.models import Order, OrderItem, Supplier
from .models import SupplierProfile, DeliveryNotification, SupplierPerformance
from .forms import OrderStatusUpdateForm, DeliveryNotificationForm, SupplierProfileUpdateForm, OrderSearchForm

from functools import wraps


def supplier_required(view_func):
    """
    Decorator to ensure the user has a supplier profile.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        try:
            if not hasattr(request.user, 'supplier_profile'):
                messages.error(request, "You need a supplier profile to access this page.")
                return redirect('landing_page')
        except SupplierProfile.DoesNotExist:
            messages.error(request, "You need a supplier profile to access this page.")
            return redirect('landing_page')
        
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view


@login_required
@supplier_required
def supplier_dashboard(request):
    """
    Dashboard view for suppliers.
    """
    supplier = request.user.supplier_profile.supplier
    
    # Get summary statistics
    pending_orders = Order.objects.filter(supplier=supplier, status='pending').count()
    shipped_orders = Order.objects.filter(supplier=supplier, status='shipped').count()
    delivered_orders = Order.objects.filter(supplier=supplier, status='delivered').count()
    
    # Get recent orders
    recent_orders = Order.objects.filter(supplier=supplier).order_by('-order_date')[:5]
    
    # Performance metrics
    try:
        performance = SupplierPerformance.objects.filter(
            supplier=supplier
        ).order_by('-period_end').first()
    except SupplierPerformance.DoesNotExist:
        performance = None
    
    context = {
        'supplier': supplier,
        'pending_orders': pending_orders,
        'shipped_orders': shipped_orders,
        'delivered_orders': delivered_orders,
        'recent_orders': recent_orders,
        'performance': performance,
    }
    
    return render(request, 'supplier/supplier_dashboard.html', context)


@login_required
@supplier_required
def view_orders(request):
    """
    View to display all orders for a supplier.
    """
    supplier = request.user.supplier_profile.supplier
    
    # Initialize search form
    form = OrderSearchForm(request.GET)
    
    # Base query
    orders = Order.objects.filter(supplier=supplier)
    
    # Apply filters if form is valid
    if form.is_valid():
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        status = form.cleaned_data.get('status')
        
        if start_date:
            orders = orders.filter(order_date__gte=start_date)
        
        if end_date:
            orders = orders.filter(order_date__lte=end_date)
        
        if status:
            orders = orders.filter(status=status)
    
    # Pagination
    paginator = Paginator(orders.order_by('-order_date'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form': form,
    }
    
    return render(request, 'supplier/view_orders.html', context)


@login_required
@supplier_required
def order_details(request, order_id):
    """
    View to display the details of an order.
    """
    supplier = request.user.supplier_profile.supplier
    order = get_object_or_404(Order, id=order_id, supplier=supplier)
    order_items = OrderItem.objects.filter(order=order).select_related('inventory')
    
    # Check if a delivery notification exists
    try:
        delivery_notification = order.delivery_notification
    except DeliveryNotification.DoesNotExist:
        delivery_notification = None
    
    context = {
        'order': order,
        'order_items': order_items,
        'delivery_notification': delivery_notification,
    }
    
    return render(request, 'supplier/order_details.html', context)


@login_required
@supplier_required
def update_delivery_status(request, order_id):
    """
    View to update the delivery status of an order.
    """
    supplier = request.user.supplier_profile.supplier
    order = get_object_or_404(Order, id=order_id, supplier=supplier)
    
    # Prevent updating cancelled orders
    if order.status == 'cancelled':
        messages.error(request, "Cannot update a cancelled order.")
        return redirect('supplier:order_details', order_id=order.id)
    
    if request.method == 'POST':
        form = OrderStatusUpdateForm(request.POST, instance=order)
        notification_form = DeliveryNotificationForm(request.POST)
        
        if form.is_valid():
            with transaction.atomic():
                # Update order status
                updated_order = form.save()
                
                # Create or update delivery notification if status is 'shipped' or 'delivered'
                if updated_order.status in ['shipped', 'delivered'] and notification_form.is_valid():
                    try:
                        notification = order.delivery_notification
                        notification_form = DeliveryNotificationForm(request.POST, instance=notification)
                        notification_form.save()
                    except DeliveryNotification.DoesNotExist:
                        notification = notification_form.save(commit=False)
                        notification.order = order
                        notification.save()
            
            messages.success(request, "Order status updated successfully.")
            return redirect('supplier:order_details', order_id=order.id)
    else:
        form = OrderStatusUpdateForm(instance=order)
        
        # Initialize notification form with existing data if available
        try:
            notification = order.delivery_notification
            notification_form = DeliveryNotificationForm(instance=notification)
        except DeliveryNotification.DoesNotExist:
            notification_form = DeliveryNotificationForm(initial={
                'delivery_date': order.expected_delivery
            })
    
    context = {
        'order': order,
        'form': form,
        'notification_form': notification_form,
    }
    
    return render(request, 'supplier/update_delivery.html', context)


@login_required
@supplier_required
def past_orders(request):
    """
    View to display past (delivered) orders.
    """
    supplier = request.user.supplier_profile.supplier
    
    # Get all delivered orders
    delivered_orders = Order.objects.filter(
        supplier=supplier,
        status='delivered'
    ).order_by('-order_date')
    
    # Pagination
    paginator = Paginator(delivered_orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'supplier/past_orders.html', {'page_obj': page_obj})


@login_required
@supplier_required
def supplier_profile(request):
    """
    View to allow suppliers to update their profile information.
    """
    supplier = request.user.supplier_profile.supplier
    
    if request.method == 'POST':
        form = SupplierProfileUpdateForm(request.POST, instance=supplier)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('supplier:supplier_dashboard')
    else:
        form = SupplierProfileUpdateForm(instance=supplier)
    
    return render(request, 'supplier/supplier_profile.html', {'form': form})


@login_required
@supplier_required
def performance_metrics(request):
    """
    View to display performance metrics for a supplier.
    """
    supplier = request.user.supplier_profile.supplier
    
    # Get performance metrics for the last 6 months
    performance_data = SupplierPerformance.objects.filter(
        supplier=supplier
    ).order_by('-period_end')[:6]
    
    # Calculate current month's statistics
    current_month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    current_month_orders = Order.objects.filter(
        supplier=supplier,
        order_date__gte=current_month_start
    )
    
    total_current_month = current_month_orders.count()
    on_time_current_month = current_month_orders.filter(
        status='delivered',
        expected_delivery__gte=F('order_date')
    ).count()
    
    if total_current_month > 0:
        on_time_percentage = (on_time_current_month / total_current_month) * 100
    else:
        on_time_percentage = 0
    
    context = {
        'performance_data': performance_data,
        'total_current_month': total_current_month,
        'on_time_current_month': on_time_current_month,
        'on_time_percentage': on_time_percentage,
    }
    
    return render(request, 'supplier/performance_metrics.html', context)