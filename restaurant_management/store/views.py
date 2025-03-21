from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.contrib import messages
from django.db.models import Sum, Count, F, Q
from django.utils import timezone
from django.http import JsonResponse, HttpResponseForbidden
from rest_framework import generics
import csv
import datetime

from django.contrib.auth.models import User  # Add this import statement
from .models import Inventory, Supplier, Order, OrderItem, Transaction, UserProfile
from .serializers import InventorySerializer
from .forms import (
    UserLoginForm, UserRegisterForm, UserUpdateForm, UserProfileForm,
    InventoryForm, SupplierForm, OrderForm, OrderItemFormSet,
    TransactionForm, DateRangeForm, ExportForm
)

class InventoryListCreateView(generics.ListCreateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer

# Custom decorator to check user roles
def role_required(roles):
    def decorator(view_func):
        @login_required
        def wrapped_view(request, *args, **kwargs):
            try:
                profile = request.user.profile
                if profile.role in roles:
                    return view_func(request, *args, **kwargs)
                else:
                    messages.error(request, "You don't have permission to access this page.")
                    return redirect('store:redirect_to_dashboard')
            except UserProfile.DoesNotExist:
                messages.error(request, "User profile not found.")
                return redirect('landing')
        return wrapped_view
    return decorator

# Authentication views
def store_login(request):
    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            # user = authenticate(username=username, password=password)
            # if user is not None:
            user = User.objects.first()  # Automatically log in the first user for testing
            try:
                profile = user.profile
            except UserProfile.DoesNotExist:
                profile = UserProfile.objects.create(user=user, role='staff')  # Create a default profile if it does not exist
            if profile.role != 'supplier':  # Suppliers use a different login
                login(request, user)
                messages.success(request, f'Welcome, {user.first_name}!')
                return redirect('store:redirect_to_dashboard')
            else:
                messages.error(request, 'Please use the supplier login.')
            # else:
            #     messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()
    return render(request, 'store/login.html', {'form': form})

@login_required
def redirect_to_dashboard(request):
    try:
        profile = request.user.profile
        if profile.role == 'admin':
            return redirect('store:admin_dashboard')
        elif profile.role == 'manager':
            return redirect('store:manager_dashboard')
        elif profile.role == 'staff':
            return redirect('store:staff_dashboard')
        else:
            messages.error(request, "Invalid user role.")
            return redirect('landing')
    except UserProfile.DoesNotExist:
        messages.error(request, "User profile not found.")
        return redirect('landing')

# Dashboard views
@login_required
@role_required(['admin'])
def admin_dashboard(request):
    # Get summary statistics for admin dashboard
    total_inventory = Inventory.objects.count()
    low_stock_items = Inventory.objects.filter(quantity__lte=F('reorder_level')).count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    
    # Get recent activities (transactions)
    recent_transactions = Transaction.objects.order_by('-created_at')[:10]
    
    context = {
        'total_inventory': total_inventory,
        'low_stock_items': low_stock_items,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'recent_transactions': recent_transactions,
    }
    
    return render(request, 'store/dashboard/admin.html', context)

@login_required
@role_required(['manager'])
def manager_dashboard(request):
    # Get summary statistics for manager dashboard
    total_inventory = Inventory.objects.count()
    low_stock_items = Inventory.objects.filter(quantity__lte=F('reorder_level')).count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='pending').count()
    
    # Get recent orders
    recent_orders = Order.objects.order_by('-order_date')[:5]
    
    # Get expiring inventory
    today = timezone.now().date()
    next_week = today + datetime.timedelta(days=7)
    expiring_soon = Inventory.objects.filter(expiry_date__range=[today, next_week])
    
    context = {
        'total_inventory': total_inventory,
        'low_stock_items': low_stock_items,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'recent_orders': recent_orders,
        'expiring_soon': expiring_soon,
    }
    
    return render(request, 'store/dashboard/manager.html', context)

@login_required
@role_required(['staff'])
def staff_dashboard(request):
    # Get summary statistics for staff dashboard
    low_stock_items = Inventory.objects.filter(quantity__lte=F('reorder_level'))
    
    # Get recent transactions by this staff member
    recent_transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'low_stock_items': low_stock_items,
        'recent_transactions': recent_transactions,
    }
    
    return render(request, 'store/dashboard/staff.html', context)

# Inventory views
@login_required
def inventory_list(request):
    inventory = Inventory.objects.all()
    
    # Filter by category if provided
    category = request.GET.get('category', '')
    if category:
        inventory = inventory.filter(category=category)
    
    # Search by name if provided
    search = request.GET.get('search', '')
    if search:
        inventory = inventory.filter(item_name__icontains=search)
    
    # Get unique categories for filter dropdown
    categories = Inventory.objects.values_list('category', flat=True).distinct()
    
    context = {
        'inventory': inventory,
        'categories': categories,
        'current_category': category,
        'search_query': search,
    }
    
    return render(request, 'store/inventory/list.html', context)

@login_required
@role_required(['admin', 'manager'])
def inventory_add(request):
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            inventory = form.save()
            
            # Record the transaction
            Transaction.objects.create(
                inventory=inventory,
                user=request.user,
                quantity_used=inventory.quantity,
                transaction_type='added'
            )
            
            messages.success(request, f'{inventory.item_name} has been added to inventory.')
            return redirect('store:inventory_list')
    else:
        form = InventoryForm()
    
    return render(request, 'store/inventory/add.html', {'form': form})

@login_required
@role_required(['admin', 'manager'])
def inventory_edit(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    old_quantity = inventory.quantity
    
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=inventory)
        if form.is_valid():
            inventory = form.save()
            
            # Record the transaction if quantity changed
            new_quantity = inventory.quantity
            if new_quantity != old_quantity:
                transaction_type = 'added' if new_quantity > old_quantity else 'removed'
                quantity_change = abs(new_quantity - old_quantity)
                
                Transaction.objects.create(
                    inventory=inventory,
                    user=request.user,
                    quantity_used=quantity_change,
                    transaction_type=transaction_type
                )
            
            messages.success(request, f'{inventory.item_name} has been updated.')
            return redirect('store:inventory_list')
    else:
        form = InventoryForm(instance=inventory)
    
    return render(request, 'store/inventory/edit.html', {'form': form, 'inventory': inventory})

@login_required
@role_required(['admin', 'manager'])
def inventory_delete(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    
    if request.method == 'POST':
        inventory_name = inventory.item_name
        inventory.delete()
        messages.success(request, f'{inventory_name} has been deleted from inventory.')
        return redirect('store:inventory_list')
    
    return render(request, 'store/inventory/delete.html', {'inventory': inventory})

@login_required
def inventory_low_stock(request):
    low_stock = Inventory.objects.filter(quantity__lte=F('reorder_level'))
    
    return render(request, 'store/inventory/low_stock.html', {'inventory': low_stock})

@login_required
def inventory_expiring(request):
    today = timezone.now().date()
    next_month = today + datetime.timedelta(days=30)
    expiring = Inventory.objects.filter(expiry_date__range=[today, next_month])
    
    return render(request, 'store/inventory/expiring.html', {'inventory': expiring})

# Order views
@login_required
def orders_list(request):
    # Filter orders based on user role
    try:
        profile = request.user.profile
        if profile.role == 'admin':
            orders = Order.objects.all()
        elif profile.role == 'manager':
            orders = Order.objects.all()
        else:  # Staff
            orders = Order.objects.filter(created_by=request.user)
    except UserProfile.DoesNotExist:
        orders = Order.objects.none()
    
    # Filter by status if provided
    status = request.GET.get('status', '')
    if status:
        orders = orders.filter(status=status)
    
    # Filter by supplier if provided
    supplier_id = request.GET.get('supplier', '')
    if supplier_id:
        orders = orders.filter(supplier_id=supplier_id)
    
    # Get suppliers for filter dropdown
    suppliers = Supplier.objects.all()
    
    context = {
        'orders': orders,
        'suppliers': suppliers,
        'current_status': status,
        'current_supplier': supplier_id,
    }
    
    return render(request, 'store/orders/list.html', context)

@login_required
@role_required(['admin', 'manager', 'staff'])
def order_add(request):
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            
            formset = OrderItemFormSet(request.POST, instance=order)
            if formset.is_valid():
                formset.save()
                messages.success(request, f'Order #{order.id} has been created.')
                
                # Check if user is staff, and redirect accordingly
                try:
                    profile = request.user.profile
                    if profile.role == 'staff':
                        return redirect('store:staff_dashboard')
                    else:
                        return redirect('store:orders_list')
                except UserProfile.DoesNotExist:
                    return redirect('store:orders_list')
            else:
                # If formset is invalid, delete the order and show errors
                order.delete()
    else:
        form = OrderForm()
        formset = OrderItemFormSet()
    
    context = {
        'form': form,
        'formset': formset,
    }
    
    return render(request, 'store/orders/create.html', context)

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order, pk=pk)
    items = order.items.all()
    
    context = {
        'order': order,
        'items': items,
    }
    
    return render(request, 'store/orders/detail.html', context)

@login_required
@role_required(['admin', 'manager'])
def order_edit(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            order = form.save()
            
            formset = OrderItemFormSet(request.POST, instance=order)
            if formset.is_valid():
                formset.save()
                messages.success(request, f'Order #{order.id} has been updated.')
                return redirect('store:orders_list')
    else:
        form = OrderForm(instance=order)
        formset = OrderItemFormSet(instance=order)
    
    context = {
        'form': form,
        'formset': formset,
        'order': order,
    }
    
    return render(request, 'store/orders/edit.html', context)

@login_required
@role_required(['admin', 'manager'])
def order_delete(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == 'POST':
        order_id = order.id
        order.delete()
        messages.success(request, f'Order #{order_id} has been deleted.')
        return redirect('store:orders_list')
    
    return render(request, 'store/orders/delete.html', {'order': order})

@login_required
@role_required(['admin', 'manager'])
def order_approve(request, pk):
    order = get_object_or_404(Order, pk=pk)
    
    if request.method == 'POST':
        order.status = 'pending'  # Update to pending to send to supplier
        order.save()
        messages.success(request, f'Order #{order.id} has been approved and sent to supplier.')
        return redirect('store:orders_list')
    
    return render(request, 'store/orders/approve.html', {'order': order})

# Transaction views
@login_required
def transactions_list(request):
    # Filter transactions based on user role
    try:
        profile = request.user.profile
        if profile.role == 'admin' or profile.role == 'manager':
            transactions = Transaction.objects.all()
        else:  # Staff
            transactions = Transaction.objects.filter(user=request.user)
    except UserProfile.DoesNotExist:
        transactions = Transaction.objects.none()
    
    # Filter by date range if provided
    if request.method == 'GET' and 'start_date' in request.GET and 'end_date' in request.GET:
        form = DateRangeForm(request.GET)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            # Add time to end_date to include the entire day
            end_date = datetime.datetime.combine(end_date, datetime.time.max)
            
            transactions = transactions.filter(created_at__range=[start_date, end_date])
    else:
        form = DateRangeForm()
    
    # Filter by transaction type if provided
    transaction_type = request.GET.get('type', '')
    if transaction_type:
        transactions = transactions.filter(transaction_type=transaction_type)
    
    context = {
        'transactions': transactions,
        'form': form,
        'current_type': transaction_type,
    }
    
    return render(request, 'store/transactions/list.html', context)

@login_required
@role_required(['admin', 'manager', 'staff'])
def transaction_add(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            
            # Get the inventory item
            inventory = transaction.inventory
            
            # Update inventory quantity based on transaction type
            if transaction.transaction_type == 'added':
                inventory.quantity += transaction.quantity_used
            elif transaction.transaction_type == 'removed':
                if inventory.quantity >= transaction.quantity_used:
                    inventory.quantity -= transaction.quantity_used
                else:
                    messages.error(request, f'Not enough {inventory.item_name} in stock.')
                    return render(request, 'store/transactions/add.html', {'form': form})
            elif transaction.transaction_type == 'adjusted':
                # Adjusted just logs the change without affecting inventory
                pass
            
            # Save inventory and transaction
            inventory.save()
            transaction.save()
            
            messages.success(request, 'Transaction recorded successfully.')
            
            # Redirect based on user role
            try:
                profile = request.user.profile
                if profile.role == 'staff':
                    return redirect('store:staff_dashboard')
                else:
                    return redirect('store:transactions_list')
            except UserProfile.DoesNotExist:
                return redirect('store:transactions_list')
    else:
        form = TransactionForm()
    
    return render(request, 'store/transactions/add.html', {'form': form})

# User Management views
@login_required
@role_required(['admin'])
def users_list(request):
    # Get all users except superusers
    from django.contrib.auth.models import User
    users = User.objects.filter(is_superuser=False)
    
    return render(request, 'store/users/list.html', {'users': users})

@login_required
@role_required(['admin'])
def user_add(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Create user profile
            role = form.cleaned_data.get('role')
            UserProfile.objects.create(user=user, role=role)
            
            messages.success(request, f'User account for {user.username} has been created.')
            return redirect('store:users_list')
    else:
        form = UserRegisterForm()
    
    return render(request, 'store/users/add.html', {'form': form})

@login_required
@role_required(['admin'])
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user, role='staff')
    
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, f'User account for {user.username} has been updated.')
            return redirect('store:users_list')
    else:
        user_form = UserUpdateForm(instance=user)
        profile_form = UserProfileForm(instance=profile)
    
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        'user': user,
    }
    
    return render(request, 'store/users/edit.html', context)

@login_required
@role_required(['admin'])
def user_delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    
    if request.method == 'POST':
        username = user.username
        user.delete()
        messages.success(request, f'User account for {username} has been deleted.')
        return redirect('store:users_list')
    
    return render(request, 'store/users/delete.html', {'user': user})

# Supplier Management views
@login_required
@role_required(['admin', 'manager'])
def suppliers_list(request):
    suppliers = Supplier.objects.all()
    
    return render(request, 'store/suppliers/list.html', {'suppliers': suppliers})

@login_required
@role_required(['admin', 'manager'])
def supplier_add(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, f'Supplier {supplier.name} has been added.')
            return redirect('store:suppliers_list')
    else:
        form = SupplierForm()
    
    return render(request, 'store/suppliers/add.html', {'form': form})

@login_required
@role_required(['admin', 'manager'])
def supplier_edit(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    
    if request.method == 'POST':
        form = SupplierForm(request.POST, instance=supplier)
        if form.is_valid():
            supplier = form.save()
            messages.success(request, f'Supplier {supplier.name} has been updated.')
            return redirect('store:suppliers_list')
    else:
        form = SupplierForm(instance=supplier)
    
    return render(request, 'store/suppliers/edit.html', {'form': form, 'supplier': supplier})

@login_required
@role_required(['admin', 'manager'])
def supplier_delete(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    
    if request.method == 'POST':
        supplier_name = supplier.name
        supplier.delete()
        messages.success(request, f'Supplier {supplier_name} has been deleted.')
        return redirect('store:suppliers_list')
    
    return render(request, 'store/suppliers/delete.html', {'supplier': supplier})

@login_required
@role_required(['admin', 'manager'])
def supplier_performance(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    
    # Get orders for this supplier
    orders = Order.objects.filter(supplier=supplier)
    
    # Get delivery statistics
    delivered_orders = orders.filter(status='delivered')
    total_orders = orders.count()
    on_time_deliveries = 0
    
    for order in delivered_orders:
        # Calculate if delivery was on time
        if order.expected_delivery and order.order_date and order.expected_delivery >= order.order_date.date():
            on_time_deliveries += 1
    
    # Calculate percentages
    if total_orders > 0:
        delivery_rate = (delivered_orders.count() / total_orders) * 100
    else:
        delivery_rate = 0
    
    if delivered_orders.count() > 0:
        on_time_rate = (on_time_deliveries / delivered_orders.count()) * 100
    else:
        on_time_rate = 0
    
    context = {
        'supplier': supplier,
        'orders': orders,
        'total_orders': total_orders,
        'delivered_orders': delivered_orders.count(),
        'delivery_rate': delivery_rate,
        'on_time_rate': on_time_rate,
    }
    
    return render(request, 'store/suppliers/performance.html', context)

# Report views
@login_required
@role_required(['admin', 'manager'])
def report_stock(request):
    inventory = Inventory.objects.all()
    
    # Group by category
    categories = {}
    for item in inventory:
        category = item.category or 'Uncategorized'
        if category not in categories:
            categories[category] = {
                'items': [],
                'total_quantity': 0,
                'low_stock_count': 0,
            }
        
        categories[category]['items'].append(item)
        categories[category]['total_quantity'] += item.quantity
        if item.is_low_stock():
            categories[category]['low_stock_count'] += 1
    
    # Summary statistics
    total_items = inventory.count()
    total_quantity = inventory.aggregate(Sum('quantity'))['quantity__sum'] or 0
    low_stock_count = inventory.filter(quantity__lte=F('reorder_level')).count()
    
    # Export form
    export_form = ExportForm()
    
    context = {
        'categories': categories,
        'total_items': total_items,
        'total_quantity': total_quantity,
        'low_stock_count': low_stock_count,
        'export_form': export_form,
    }
    
    return render(request, 'store/reports/stock.html', context)

@login_required
@role_required(['admin', 'manager'])
def report_orders(request):
    # Date range filter
    if request.method == 'GET' and 'start_date' in request.GET and 'end_date' in request.GET:
        form = DateRangeForm(request.GET)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            orders = Order.objects.filter(order_date__date__range=[start_date, end_date])
        else:
            orders = Order.objects.all()
    else:
        form = DateRangeForm()
        orders = Order.objects.all()
    
    # Group by status
    status_counts = orders.values('status').annotate(count=Count('status'))
    
    # Group by supplier
    supplier_counts = orders.values('supplier__name').annotate(count=Count('supplier'))
    
    # Export form
    export_form = ExportForm()
    
    context = {
        'orders': orders,
        'status_counts': status_counts,
        'supplier_counts': supplier_counts,
        'form': form,
        'export_form': export_form,
    }
    
    return render(request, 'store/reports/orders.html', context)

@login_required
@role_required(['admin', 'manager'])
def report_suppliers(request):
    suppliers = Supplier.objects.all()
    supplier_data = []
    
    for supplier in suppliers:
        orders = Order.objects.filter(supplier=supplier)
        total_orders = orders.count()
        delivered = orders.filter(status='delivered').count()
        pending = orders.filter(status='pending').count()
        
        supplier_data.append({
            'supplier': supplier,
            'total_orders': total_orders,
            'delivered': delivered,
            'pending': pending,
        })
    
    # Export form
    export_form = ExportForm()
    
    context = {
        'supplier_data': supplier_data,
        'export_form': export_form,
    }
    
    return render(request, 'store/reports/suppliers.html', context)

@login_required
@role_required(['admin', 'manager'])
def report_export(request, report_type):
    # Determine export format
    export_format = request.GET.get('format', 'csv')
    
    # Generate appropriate data based on report type
    if report_type == 'stock':
        data = Inventory.objects.all()
        filename = f'stock_report_{timezone.now().strftime("%Y%m%d")}'
        headers = ['ID', 'Item Name', 'Category', 'Quantity', 'Reorder Level', 'Expiry Date', 'Supplier']
        
        if export_format == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
            
            writer = csv.writer(response)
            writer.writerow(headers)
            
            for item in data:
                writer.writerow([
                    item.id,
                    item.item_name,
                    item.category,
                    item.quantity,
                    item.reorder_level,
                    item.expiry_date,
                    item.supplier.name if item.supplier else 'N/A'
                ])
            
            return response
        else:
            # For PDF, just return a message for now
            return HttpResponse("PDF export will be implemented in the future.")
            
    elif report_type == 'orders':
        data = Order.objects.all()
        filename = f'orders_report_{timezone.now().strftime("%Y%m%d")}'
        headers = ['Order ID', 'Supplier', 'Status', 'Order Date', 'Expected Delivery']
        
        if export_format == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
            
            writer = csv.writer(response)
            writer.writerow(headers)
            
            for order in data:
                writer.writerow([
                    order.id,
                    order.supplier.name,
                    order.status,
                    order.order_date,
                    order.expected_delivery
                ])
            
            return response
        else:
            # For PDF, just return a message for now
            return HttpResponse("PDF export will be implemented in the future.")
            
    elif report_type == 'suppliers':
        data = Supplier.objects.all()
        filename = f'suppliers_report_{timezone.now().strftime("%Y%m%d")}'
        headers = ['ID', 'Name', 'Contact Info', 'Email', 'Phone', 'Total Orders']
        
        if export_format == 'csv':
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = f'attachment; filename="{filename}.csv"'
            
            writer = csv.writer(response)
            writer.writerow(headers)
            
            for supplier in data:
                total_orders = Order.objects.filter(supplier=supplier).count()
                writer.writerow([
                    supplier.id,
                    supplier.name,
                    supplier.contact_info,
                    supplier.email,
                    supplier.phone,
                    total_orders
                ])
            
            return response
        else:
            # For PDF, just return a message for now
            return HttpResponse("PDF export will be implemented in the future.")
    
    # If report type is not recognized
    return HttpResponseForbidden("Invalid report type")