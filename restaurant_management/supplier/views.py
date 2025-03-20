from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Count, Q
import datetime

from store.models import Supplier, Order, OrderItem
from store.models import UserProfile
from .models import SupplierExtended
from .forms import (
    SupplierLoginForm, OrderStatusUpdateForm, SupplierProfileForm,
    DateRangeFilterForm, OrderFilterForm
)

# Custom decorator to check if user is a supplier
def supplier_required(view_func):
    @login_required
    def wrapped_view(request, *args, **kwargs):
        try:
            profile = request.user.profile
            if profile.role == 'supplier':
                return view_func(request, *args, **kwargs)
            else:
                messages.error(request, "You don't have permission to access this page.")
                return redirect('store:redirect_to_dashboard')
        except UserProfile.DoesNotExist:
            messages.error(request, "User profile not found.")
            return redirect('landing')
    return wrapped_view

# Helper function to get supplier for user
def get_supplier_for_user(user):
    try:
        # Check if user is a supplier with associated supplier
        profile = user.profile
        if profile.role == 'supplier' and profile.supplier:
            return profile.supplier
    except (UserProfile.DoesNotExist, AttributeError):
        pass
    return None

# Authentication views
def supplier_login(request):
    if request.method == 'POST':
        form = SupplierLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                # Ensure the user has a profile
                if hasattr(user, 'profile'):
                    profile = user.profile
                    if profile.role == 'supplier':
                        messages.success(request, f'Welcome, {user.first_name}!')
                        return redirect('supplier:dashboard')
                    else:
                        messages.error(request, 'Please use the store login.')
                else:
                    messages.error(request, 'User profile not found.')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = SupplierLoginForm()
    return render(request, 'supplier/login.html', {'form': form})

# Dashboard view
@login_required
@supplier_required
def supplier_dashboard(request):
    supplier = get_supplier_for_user(request.user)
    
    if not supplier:
        messages.error(request, "No supplier associated with this account.")
        return redirect('landing')
    
    # Get supplier extended object to use custom methods
    supplier_ext = SupplierExtended.objects.get(pk=supplier.pk)
    
    # Get summary statistics
    total_orders = supplier_ext.get_all_orders().count()
    pending_orders = supplier_ext.get_orders_by_status('pending').count()
    
    # Get recent orders
    recent_orders = supplier_ext.get_all_orders().order_by('-order_date')[:5]
    
    context = {
        'supplier': supplier,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'recent_orders': recent_orders,
    }
    
    return render(request, 'supplier/dashboard.html', context)

# Orders views
@login_required
@supplier_required
def orders_list(request):
    supplier = get_supplier_for_user(request.user)
    
    if not supplier:
        messages.error(request, "No supplier associated with this account.")
        return redirect('supplier:dashboard')
    
    # Get orders for this supplier
    orders = Order.objects.filter(supplier=supplier)
    
    # Filter by status if provided
    status_filter = request.GET.get('status', '')
    if status_filter:
        orders = orders.filter(status=status_filter)
    
    # Filter by date range if provided
    date_filter_form = DateRangeFilterForm(request.GET or None)
    if date_filter_form.is_valid():
        start_date = date_filter_form.cleaned_data.get('start_date')
        end_date = date_filter_form.cleaned_data.get('end_date')
        
        if start_date:
            orders = orders.filter(order_date__date__gte=start_date)
        if end_date:
            # Add time to end_date to include the entire day
            end_datetime = datetime.datetime.combine(end_date, datetime.time.max)
            orders = orders.filter(order_date__lte=end_datetime)
    
    # Order filter form
    order_filter_form = OrderFilterForm(request.GET or None)
    
    context = {
        'orders': orders,
        'date_filter_form': date_filter_form,
        'order_filter_form': order_filter_form,
        'current_status': status_filter,
    }
    
    return render(request, 'supplier/orders/list.html', context)

@login_required
@supplier_required
def order_detail(request, pk):
    supplier = get_supplier_for_user(request.user)
    
    if not supplier:
        messages.error(request, "No supplier associated with this account.")
        return redirect('supplier:dashboard')
    
    # Get order if it belongs to this supplier
    order = get_object_or_404(Order, pk=pk, supplier=supplier)
    items = order.items.all()
    
    context = {
        'order': order,
        'items': items,
    }
    
    return render(request, 'supplier/orders/detail.html', context)

@login_required
@supplier_required
def order_update_status(request, pk):
    supplier = get_supplier_for_user(request.user)
    
    if not supplier:
        messages.error(request, "No supplier associated with this account.")
        return redirect('supplier:dashboard')
    
    # Get order if it belongs to this supplier
    order = get_object_or_404(Order, pk=pk, supplier=supplier)
    
    if request.method == 'POST':
        form = OrderStatusUpdateForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()
            messages.success(request, f'Order #{order.id} status has been updated to {order.get_status_display()}.')
            return redirect('supplier:orders_list')
    else:
        form = OrderStatusUpdateForm(instance=order)
    
    context = {
        'form': form,
        'order': order,
    }
    
    return render(request, 'supplier/delivery/update.html', context)

@login_required
@supplier_required
def orders_history(request):
    supplier = get_supplier_for_user(request.user)
    
    if not supplier:
        messages.error(request, "No supplier associated with this account.")
        return redirect('supplier:dashboard')
    
    # Get all completed orders for this supplier
    orders = Order.objects.filter(
        supplier=supplier
    ).exclude(
        status='pending'
    ).order_by('-order_date')
    
    # Filter by date range if provided
    date_filter_form = DateRangeFilterForm(request.GET or None)
    if date_filter_form.is_valid():
        start_date = date_filter_form.cleaned_data.get('start_date')
        end_date = date_filter_form.cleaned_data.get('end_date')
        
        if start_date:
            orders = orders.filter(order_date__date__gte=start_date)
        if end_date:
            # Add time to end_date to include the entire day
            end_datetime = datetime.datetime.combine(end_date, datetime.time.max)
            orders = orders.filter(order_date__lte=end_datetime)
    
    # Group orders by month for summary
    # Will use annotation for this
    from django.db.models.functions import TruncMonth
    
    monthly_orders = orders.annotate(
        month=TruncMonth('order_date')
    ).values('month').annotate(
        count=Count('id')
    ).order_by('-month')
    
    context = {
        'orders': orders,
        'monthly_orders': monthly_orders,
        'date_filter_form': date_filter_form,
    }
    
    return render(request, 'supplier/orders/history.html', context)

# Profile views
@login_required
@supplier_required
def supplier_profile(request):
    supplier = get_supplier_for_user(request.user)
    
    if not supplier:
        messages.error(request, "No supplier associated with this account.")
        return redirect('landing')
    
    context = {
        'supplier': supplier,
    }
    
    return render(request, 'supplier/profile.html', context)

@login_required
@supplier_required
def supplier_profile_edit(request):
    supplier = get_supplier_for_user(request.user)
    
    if not supplier:
        messages.error(request, "No supplier associated with this account.")
        return redirect('landing')
    
    if request.method == 'POST':
        form = SupplierProfileForm(request.POST, instance=supplier)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('supplier:profile')
    else:
        form = SupplierProfileForm(instance=supplier)
    
    context = {
        'form': form,
        'supplier': supplier,
    }
    
    return render(request, 'supplier/profile_edit.html', context)