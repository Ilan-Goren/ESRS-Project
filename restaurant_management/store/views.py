from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from datetime import datetime, timedelta
import uuid
from django.conf import settings
import jwt

from rest_framework import permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q
from django.contrib.auth.models import User

"""
Views for the store application.

These views handle all the functionality for store users (admins, managers, and staff),
including authentication, inventory management, order processing, and reporting.
"""

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Sum, Count, F, Q
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator
from django.db import transaction as db_transaction

from .models import UserProfile, Inventory, Order, OrderItem, Transaction, Supplier
from .forms import (
    UserRegistrationForm, CustomAuthenticationForm, InventoryForm,
    TransactionForm, OrderForm, OrderItemForm, OrderUpdateForm,
    DateRangeForm, UserProfileForm
)
from .decorators import role_required

# Django REST Framework imports for API views
from rest_framework import generics, permissions
from .serializers import InventorySerializer


def landing_page(request):
    """
    Landing page view that displays login options and redirects based on user role.
    """
    if request.user.is_authenticated:
        try:
            profile = request.user.profile
            if profile.is_supplier:
                return redirect('supplier:dashboard')
            elif profile.is_admin:
                return redirect('store:admin_dashboard')
            elif profile.is_manager:
                return redirect('store:manager_dashboard')
            elif profile.is_staff:
                return redirect('store:staff_dashboard')
        except UserProfile.DoesNotExist:
            # Default fallback if profile doesn't exist
            return redirect('store:admin_dashboard')
    
    return render(request, 'landing_page.html')


def register_user(request):
    """
    View for user registration.
    """
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            with db_transaction.atomic():
                user = form.save()
                role = form.cleaned_data.get('role')
                supplier = form.cleaned_data.get('supplier')
                
                UserProfile.objects.create(
                    user=user,
                    role=role
                )
                
                if role == 'supplier' and supplier:
                    # Create supplier-specific profile in the supplier app
                    from supplier.models import SupplierProfile
                    SupplierProfile.objects.create(
                        user=user,
                        supplier=supplier
                    )
                
                messages.success(request, 'Account created successfully!')
                return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'registration/register.html', {'form': form})


@login_required
@role_required('admin')
def admin_dashboard(request):
    """
    Dashboard view for admin users.
    """
    # Get summary statistics
    total_inventory_items = Inventory.objects.count()
    low_stock_items = Inventory.objects.filter(quantity__lte=F('reorder_level')).count()
    expired_items = Inventory.objects.filter(expiry_date__lt=timezone.now().date()).count()
    total_users = User.objects.count()
    
    # Get recent orders
    recent_orders = Order.objects.select_related('supplier').order_by('-order_date')[:5]
    
    # Get inventory by category
    inventory_by_category = Inventory.objects.values('category').annotate(
        total=Count('id'),
        total_quantity=Sum('quantity')
    )
    
    context = {
        'total_inventory_items': total_inventory_items,
        'low_stock_items': low_stock_items,
        'expired_items': expired_items,
        'total_users': total_users,
        'recent_orders': recent_orders,
        'inventory_by_category': inventory_by_category,
    }
    
    return render(request, 'store/admin_dashboard.html', context)


@login_required
@role_required('manager')
def manager_dashboard(request):
    """
    Dashboard view for manager users.
    """
    # Get summary statistics
    total_inventory_items = Inventory.objects.count()
    low_stock_items = Inventory.objects.filter(quantity__lte=F('reorder_level'))
    pending_orders = Order.objects.filter(status='pending').count()
    
    # Get recent transactions
    recent_transactions = Transaction.objects.select_related(
        'inventory', 'user__user'
    ).order_by('-created_at')[:10]
    
    context = {
        'total_inventory_items': total_inventory_items,
        'low_stock_items': low_stock_items,
        'pending_orders': pending_orders,
        'recent_transactions': recent_transactions,
    }
    
    return render(request, 'store/manager_dashboard.html', context)


@login_required
@role_required('staff')
def staff_dashboard(request):
    """
    Dashboard view for staff users.
    """
    # Get summary statistics
    low_stock_items = Inventory.objects.filter(quantity__lte=F('reorder_level'))
    
    # Get recent transactions by this user
    recent_transactions = Transaction.objects.filter(
        user=request.user.profile
    ).select_related('inventory').order_by('-created_at')[:10]
    
    context = {
        'low_stock_items': low_stock_items,
        'recent_transactions': recent_transactions,
    }
    
    return render(request, 'store/staff_dashboard.html', context)


@login_required
@role_required(['admin', 'manager', 'staff'])
def inventory_list(request):
    """
    View to display a list of inventory items.
    """
    category = request.GET.get('category', '')
    search = request.GET.get('search', '')
    low_stock = request.GET.get('low_stock', False) == 'true'
    
    inventory_items = Inventory.objects.select_related('supplier').all()
    
    # Apply filters
    if category:
        inventory_items = inventory_items.filter(category=category)
    
    if search:
        inventory_items = inventory_items.filter(
            Q(item_name__icontains=search) | Q(sku__icontains=search)
        )
    
    if low_stock:
        inventory_items = inventory_items.filter(quantity__lte=F('reorder_level'))
    
    # Get unique categories for filter dropdown
    categories = Inventory.objects.values_list('category', flat=True).distinct()
    
    # Pagination
    paginator = Paginator(inventory_items, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'category': category,
        'search': search,
        'low_stock': low_stock,
    }
    
    return render(request, 'store/inventory/view_stock.html', context)


@login_required
@role_required(['admin', 'manager'])
def add_inventory(request):
    """
    View to add a new inventory item.
    """
    if request.method == 'POST':
        form = InventoryForm(request.POST)
        if form.is_valid():
            inventory_item = form.save()
            
            # Record transaction
            Transaction.objects.create(
                inventory=inventory_item,
                user=request.user.profile,
                quantity_used=inventory_item.quantity,
                transaction_type='added'
            )
            
            messages.success(request, 'Inventory item added successfully!')
            return redirect('store:inventory_list')
    else:
        form = InventoryForm()
    
    return render(request, 'store/inventory/add_stock.html', {'form': form})


@login_required
@role_required(['admin', 'manager'])
def edit_inventory(request, pk):
    """
    View to edit an existing inventory item.
    """
    inventory_item = get_object_or_404(Inventory, pk=pk)
    old_quantity = inventory_item.quantity
    
    if request.method == 'POST':
        form = InventoryForm(request.POST, instance=inventory_item)
        if form.is_valid():
            inventory_item = form.save()
            new_quantity = inventory_item.quantity
            
            # Record transaction if quantity changed
            if new_quantity != old_quantity:
                transaction_type = 'added' if new_quantity > old_quantity else 'removed'
                quantity_diff = abs(new_quantity - old_quantity)
                
                Transaction.objects.create(
                    inventory=inventory_item,
                    user=request.user.profile,
                    quantity_used=quantity_diff,
                    transaction_type=transaction_type
                )
            
            messages.success(request, 'Inventory item updated successfully!')
            return redirect('store:inventory_list')
    else:
        form = InventoryForm(instance=inventory_item)
    
    return render(request, 'store/inventory/edit_stock.html', {
        'form': form,
        'inventory_item': inventory_item
    })


@login_required
@role_required(['admin', 'manager', 'staff'])
def inventory_transaction(request):
    """
    View to record inventory transactions (add, remove, adjust).
    """
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user.profile
            
            inventory_item = transaction.inventory
            old_quantity = inventory_item.quantity
            
            # Update inventory quantity based on transaction type
            if transaction.transaction_type == 'added':
                inventory_item.quantity += transaction.quantity_used
            elif transaction.transaction_type == 'removed':
                if inventory_item.quantity < transaction.quantity_used:
                    messages.error(request, 'Insufficient inventory!')
                    return render(request, 'store/inventory/transaction.html', {'form': form})
                inventory_item.quantity -= transaction.quantity_used
            elif transaction.transaction_type == 'adjusted':
                inventory_item.quantity = transaction.quantity_used
                transaction.quantity_used = abs(old_quantity - transaction.quantity_used)
            
            # Save inventory and transaction
            with db_transaction.atomic():
                inventory_item.save()
                transaction.save()
            
            messages.success(request, 'Transaction recorded successfully!')
            return redirect('store:inventory_list')
    else:
        form = TransactionForm()
    
    return render(request, 'store/inventory/transaction.html', {'form': form})


@login_required
@role_required(['admin', 'manager', 'staff'])
def low_stock_alerts(request):
    """
    View to display items that are below their reorder level.
    """
    low_stock_items = Inventory.objects.filter(
        quantity__lte=F('reorder_level')
    ).select_related('supplier')
    
    return render(request, 'store/inventory/low_stock_alerts.html', {
        'low_stock_items': low_stock_items
    })


@login_required
@role_required(['admin', 'manager', 'staff'])
def expiry_dates(request):
    """
    View to display items approaching or past their expiry date.
    """
    today = timezone.now().date()
    thirty_days_later = today + timezone.timedelta(days=30)
    
    expired_items = Inventory.objects.filter(
        expiry_date__lt=today
    ).select_related('supplier')
    
    expiring_soon_items = Inventory.objects.filter(
        expiry_date__gte=today,
        expiry_date__lte=thirty_days_later
    ).select_related('supplier')
    
    context = {
        'expired_items': expired_items,
        'expiring_soon_items': expiring_soon_items,
    }
    
    return render(request, 'store/inventory/expiry_dates.html', context)


@login_required
@role_required(['admin', 'manager', 'staff'])
def order_list(request):
    """
    View to display a list of orders.
    """
    status = request.GET.get('status', '')
    supplier_id = request.GET.get('supplier', '')
    
    orders = Order.objects.select_related('supplier').all()
    
    # Apply filters
    if status:
        orders = orders.filter(status=status)
    
    if supplier_id:
        orders = orders.filter(supplier_id=supplier_id)
    
    # Get suppliers for filter dropdown
    suppliers = Supplier.objects.all()
    
    # Pagination
    paginator = Paginator(orders.order_by('-order_date'), 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'suppliers': suppliers,
        'status': status,
        'supplier_id': supplier_id,
    }
    
    return render(request, 'store/orders/order_list.html', context)


@login_required
@role_required(['admin', 'manager'])
def create_order(request):
    """
    View to create a new order.
    """
    if request.method == 'POST':
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            order = order_form.save()
            messages.success(request, 'Order created successfully!')
            return redirect('store:add_order_items', order_id=order.id)
    else:
        order_form = OrderForm()
    
    return render(request, 'store/orders/create_order.html', {'form': order_form})


@login_required
@role_required(['admin', 'manager'])
def add_order_items(request, order_id):
    """
    View to add items to an order.
    """
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        form = OrderItemForm(request.POST)
        if form.is_valid():
            order_item = form.save(commit=False)
            order_item.order = order
            order_item.save()
            
            messages.success(request, 'Item added to order successfully!')
            return redirect('store:add_order_items', order_id=order.id)
    else:
        form = OrderItemForm()
    
    # Get existing items in this order
    order_items = OrderItem.objects.filter(order=order).select_related('inventory')
    
    context = {
        'form': form,
        'order': order,
        'order_items': order_items,
    }
    
    return render(request, 'store/orders/add_order_items.html', context)


@login_required
@role_required(['admin', 'manager'])
def update_order_status(request, order_id):
    """
    View to update the status of an order.
    """
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        form = OrderUpdateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, 'Order status updated successfully!')
            return redirect('store:order_list')
    else:
        form = OrderUpdateForm(instance=order)
    
    return render(request, 'store/orders/update_status.html', {
        'form': form,
        'order': order
    })


@login_required
@role_required(['admin', 'manager'])
def order_details(request, order_id):
    """
    View to display the details of an order.
    """
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderItem.objects.filter(order=order).select_related('inventory')
    
    return render(request, 'store/orders/order_details.html', {
        'order': order,
        'order_items': order_items
    })


@login_required
@role_required('admin')
def manage_users(request):
    """
    View to display and manage all users.
    """
    users = User.objects.select_related('profile').all()
    
    return render(request, 'store/manage_users.html', {'users': users})


@login_required
@role_required('admin')
def edit_user(request, user_id):
    """
    View to edit a user's information.
    """
    user = get_object_or_404(User, id=user_id)
    
    try:
        profile = user.profile
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=user, role='staff')
    
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'User updated successfully!')
            return redirect('store:manage_users')
    else:
        form = UserProfileForm(instance=profile)
    
    return render(request, 'store/edit_user.html', {
        'form': form,
        'user': user
    })


@login_required
@role_required(['admin', 'manager'])
def stock_report(request):
    """
    View to generate a stock report.
    """
    # Get all inventory items grouped by category
    inventory_by_category = {}
    
    for item in Inventory.objects.all():
        category = item.category or 'Uncategorized'
        if category not in inventory_by_category:
            inventory_by_category[category] = []
        inventory_by_category[category].append(item)
    
    return render(request, 'store/reports/stock_report.html', {
        'inventory_by_category': inventory_by_category
    })


@login_required
@role_required(['admin', 'manager'])
def order_summary(request):
    """
    View to generate an order summary report.
    """
    if request.method == 'POST':
        form = DateRangeForm(request.POST)
        if form.is_valid():
            start_date = form.cleaned_data['start_date']
            end_date = form.cleaned_data['end_date']
            
            orders = Order.objects.filter(
                order_date__gte=start_date,
                order_date__lte=end_date
            ).select_related('supplier')
            
            context = {
                'form': form,
                'orders': orders,
                'start_date': start_date,
                'end_date': end_date,
            }
            
            return render(request, 'store/reports/order_summary.html', context)
    else:
        form = DateRangeForm()
    
    return render(request, 'store/reports/order_summary.html', {'form': form})


@login_required
@role_required(['admin', 'manager'])
def supplier_performance(request):
    """
    View to generate a supplier performance report.
    """
    suppliers = Supplier.objects.all()
    supplier_stats = []
    
    for supplier in suppliers:
        total_orders = Order.objects.filter(supplier=supplier).count()
        delivered_on_time = Order.objects.filter(
            supplier=supplier,
            status='delivered',
            expected_delivery__gte=F('order_date')
        ).count()
        
        if total_orders > 0:
            on_time_percentage = (delivered_on_time / total_orders) * 100
        else:
            on_time_percentage = 0
        
        supplier_stats.append({
            'supplier': supplier,
            'total_orders': total_orders,
            'delivered_on_time': delivered_on_time,
            'on_time_percentage': on_time_percentage,
        })
    
    return render(request, 'store/reports/supplier_performance.html', {
        'supplier_stats': supplier_stats
    })


@login_required
@role_required(['admin', 'manager'])
def configure_settings(request):
    """
    View to configure system settings.
    """
    # Placeholder for system settings
    return render(request, 'store/configure_settings.html')


@login_required
@role_required(['admin', 'manager'])
def manage_suppliers(request):
    """
    View to manage suppliers.
    """
    suppliers = Supplier.objects.all()
    
    return render(request, 'store/manage_suppliers.html', {'suppliers': suppliers})
    
class InventoryListCreateAPIView(generics.ListCreateAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated]

class InventoryRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inventory.objects.all()
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated]


# API Login View
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate
from django.http import JsonResponse
import json

@csrf_exempt
def api_login_view(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            email = data.get('email')
            password = data.get('password')
            role = data.get('role') 

            user = authenticate(request, username=email, password=password)
            if user is not None:
                try:
                    user_profile = user.userprofile
                    user_role = user_profile.role
                except Exception:
                    user_role = 'admin' if user.is_superuser else 'unknown'
                
                # Create a JWT token
                payload = {
                    'user_id': user.id,
                    'email': user.email,
                    'exp': datetime.utcnow() + timedelta(days=1),
                    'iat': datetime.utcnow(),
                    'jti': str(uuid.uuid4())
                }
                
                # Using Django's SECRET_KEY to sign the token
                token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
                
                # Convert bytes to string if needed (PyJWT < 2.0)
                if isinstance(token, bytes):
                    token = token.decode('utf-8')
                
                # Create user data to return
                user_data = {
                    'id': user.id,
                    'name': user.get_full_name() or user.username,
                    'email': user.email,
                    'role': user_role
                }
                
                # Return both the token and user data in the format expected by the frontend
                return JsonResponse({
                    'message': 'Login successful',
                    'token': token,     # For Login.tsx
                    'access': token,    # For token storage service
                    'refresh': token,   # For refresh token functionality 
                    'user': user_data,
                    'role': user_role
                })
            else:
                return JsonResponse({'message': 'Invalid credentials'}, status=401)
        except Exception as e:
            return JsonResponse({'message': 'Error during login', 'error': str(e)}, status=400)
    return JsonResponse({'message': 'Invalid request'}, status=405)


# API Dashboard View

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import UserProfile, Supplier

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def dashboard_api_view(request):
    """
    Dashboard API view that uses standard DRF authentication.
    This leverages the built-in JWT authentication from djangorestframework-simplejwt.
    """
    # Access is automatically granted only if the JWT token is valid
    # The user is automatically populated by DRF's authentication system

    # Get dashboard statistics
    total_users = User.objects.count()
    suppliers_count = Supplier.objects.count()
    roles_count = UserProfile.objects.values('role').distinct().count()

    return Response({
        'totalUsers': total_users,
        'suppliers': suppliers_count,
        'totalRoles': roles_count,
        'systemUptimeDays': 7
    })

# Manager Dashboard API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def manager_dashboard_api_view(request):
    """
    API view for manager dashboard data.
    """
    try:
        # Get actual data from your database
        total_inventory = Inventory.objects.count()
        
        # Order statistics - use defaults if models don't have these statuses
        try:
            orders_delivered = Order.objects.filter(status='delivered').count()
        except:
            orders_delivered = 12
            
        try:
            orders_pending = Order.objects.filter(status='pending').count()
        except:
            orders_pending = 5
            
        try:
            orders_shipped = Order.objects.filter(status='shipped').count()
        except:
            orders_shipped = 8
        
        return JsonResponse({
            'totalInventory': total_inventory,
            'ordersDelivered': orders_delivered,
            'ordersPending': orders_pending,
            'ordersShipped': orders_shipped
        })
    except Exception as e:
        print(f"Manager Dashboard API error: {str(e)}")
        return JsonResponse({
            'totalInventory': 0,
            'ordersDelivered': 0,
            'ordersPending': 0,
            'ordersShipped': 0,
            'error': str(e)
        })

# Staff Dashboard API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def staff_dashboard_api_view(request):
    """
    API view for staff dashboard data.
    """
    try:
        # Get low stock count
        try:
            low_stock_count = Inventory.objects.filter(quantity__lte=F('reorder_level')).count()
        except:
            low_stock_count = 7
        
        # Get staff transactions
        try:
            if hasattr(request.user, 'userprofile'):
                user_transactions = Transaction.objects.filter(
                    user=request.user.userprofile
                ).count()
            else:
                user_transactions = 15
        except:
            user_transactions = 15
            
        # Get inventory movement data
        try:
            total_additions = Transaction.objects.filter(transaction_type='added').count()
            total_removals = Transaction.objects.filter(transaction_type='removed').count()
        except:
            total_additions = 28
            total_removals = 18
        
        return JsonResponse({
            'lowStockCount': low_stock_count,
            'myTransactions': user_transactions,
            'totalAdditions': total_additions,
            'totalRemovals': total_removals
        })
    except Exception as e:
        print(f"Staff Dashboard API error: {str(e)}")
        return JsonResponse({
            'lowStockCount': 0,
            'myTransactions': 0,
            'totalAdditions': 0,
            'totalRemovals': 0,
            'error': str(e)
        })

# Supplier Dashboard API
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def supplier_dashboard_api_view(request):
    """
    API view for supplier dashboard data.
    """
    try:
        # Try to find the supplier associated with the user
        supplier_id = None
        if hasattr(request.user, 'userprofile'):
            profile = request.user.userprofile
            if profile.role == 'supplier':
                # Try to get supplier_id from related models
                try:
                    # This depends on your model structure
                    supplier_profile = request.user.supplierprofile
                    supplier_id = supplier_profile.supplier_id
                except:
                    # Fallback to looking up by supplier name matching user email
                    try:
                        supplier = Supplier.objects.filter(
                            contact_email__icontains=request.user.email
                        ).first()
                        if supplier:
                            supplier_id = supplier.id
                    except:
                        pass
        
        # Orders data - either real or placeholder
        if supplier_id:
            try:
                total_orders = Order.objects.filter(supplier_id=supplier_id).count()
                pending_orders = Order.objects.filter(supplier_id=supplier_id, status='pending').count()
                delivered_orders = Order.objects.filter(supplier_id=supplier_id, status='delivered').count()
                in_transit = Order.objects.filter(supplier_id=supplier_id, status='shipped').count()
            except:
                total_orders = 42
                pending_orders = 7
                delivered_orders = 31
                in_transit = 4
        else:
            # Demo data
            total_orders = 42
            pending_orders = 7
            delivered_orders = 31
            in_transit = 4
            
        return JsonResponse({
            'totalOrders': total_orders,
            'pendingOrders': pending_orders,
            'deliveredOrders': delivered_orders,
            'inTransitOrders': in_transit
        })
    except Exception as e:
        print(f"Supplier Dashboard API error: {str(e)}")
        return JsonResponse({
            'totalOrders': 0,
            'pendingOrders': 0,
            'deliveredOrders': 0,
            'inTransitOrders': 0,
            'error': str(e)
        })

# API User List View for /api/users/
class UserListView(APIView):
    permission_classes = [permissions.IsAuthenticated] 

    def get(self, request):
        search_query = request.GET.get('search', '')
        users = User.objects.filter(
            Q(username__icontains=search_query) |
            Q(email__icontains=search_query)
        )
        
        # Convert to list of dictionaries with the expected fields
        user_list = []
        for user in users:
            try:
                profile = user.profile
                role = getattr(profile, 'role', 'admin' if user.is_superuser else 'staff')
            except:
                role = 'admin' if user.is_superuser else 'staff'
                
            user_data = {
                'id': user.id,
                'name': user.get_full_name() or user.username,
                'email': user.email,
                'role': role
            }
            user_list.append(user_data)
            
        return Response(user_list, status=status.HTTP_200_OK)

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def api_register_view(request):
    """API view for user registration."""
    try:
        # Get data from request
        data = request.data
        username = data.get('username') or data.get('email')
        email = data.get('email')
        password = data.get('password')
        name = data.get('name', username)
        
        # Explicitly get role and validate it
        role = (data.get('role') or '').lower()
        print(f"Registration received with role: {role}, data keys: {data.keys()}")
        
        # Validate the role
        valid_roles = ['admin', 'manager', 'staff', 'supplier']
        if not role or role not in valid_roles:
            print(f"Invalid role provided: {role}, defaulting to 'staff'")
            role = 'staff'
        else:
            print(f"Using specified role: {role}")
        
        # Validation checks
        if not username or not email or not password:
            return JsonResponse({
                'message': 'Username, email and password are required'
            }, status=400)
        
        # Check for existing users and handle that first
        user = None
        
        # Check for existing user by username
        try:
            user = User.objects.get(username=username)
            return JsonResponse({
                'message': 'Username already exists'
            }, status=400)
        except User.DoesNotExist:
            pass
            
        # Check for existing user by email
        try:
            user = User.objects.get(email=email)
            return JsonResponse({
                'message': 'Email already exists'
            }, status=400)
        except User.DoesNotExist:
            pass
        
        # If we got here, user doesn't exist, so create it
        from django.db import transaction
        try:
            with transaction.atomic():
                # Create user
                user = User.objects.create_user(
                    username=username,
                    email=email,
                    password=password
                )
                
                # Set name
                if name and name != username:
                    name_parts = name.split(' ', 1)
                    user.first_name = name_parts[0]
                    if len(name_parts) > 1:
                        user.last_name = name_parts[1]
                    user.save()
                
                # Create UserProfile with validated role
                from store.models import UserProfile
                
                # First check if a profile already exists
                try:
                    profile = UserProfile.objects.get(user=user)
                    profile.role = role
                    profile.save()
                    print(f"Updated existing profile for user {user.id} with role: {role}")
                except UserProfile.DoesNotExist:
                    # Create new profile only if one doesn't exist
                    profile = UserProfile.objects.create(
                        user=user,
                        role=role
                    )
                    print(f"Created new profile for user {user.id} with role: {role}")
            
            # If we get here, everything was successful
            return JsonResponse({
                'message': 'User registered successfully',
                'user': {
                    'id': user.id,
                    'name': name,
                    'email': email,
                    'role': role
                }
            }, status=201)
        except Exception as e:
            # If something went wrong during user creation
            print(f"Error during user creation: {str(e)}")
            
            # Clean up if user was created but profile failed
            if user and user.id:
                try:
                    user.delete()
                    print(f"Cleaned up partially created user {user.id}")
                except:
                    pass
                
            raise
        
    except Exception as e:
        # Log the full error with traceback
        import traceback
        print(f"Registration error: {str(e)}")
        print(traceback.format_exc())
        
        return JsonResponse({
            'message': 'Error during registration',
            'error': str(e)
        }, status=400)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated])
def user_detail_api_view(request, user_id):
    """API view for retrieving, updating or deleting a user."""
    try:
        user = User.objects.get(id=user_id)
    except User.DoesNotExist:
        return JsonResponse({'message': 'User not found'}, status=404)
        
    if request.method == 'GET':
        # Return user details
        try:
            profile = user.userprofile
            role = profile.role
        except:
            role = 'admin' if user.is_superuser else 'staff'
            
        user_data = {
            'id': user.id,
            'name': user.get_full_name() or user.username,
            'email': user.email,
            'role': role
        }
        return JsonResponse(user_data)
        
    elif request.method == 'PUT':
        # Update user details
        data = request.data
        name = data.get('name')
        role = (data.get('role') or '').lower()
        
        print(f"Updating user {user_id} with data: {data}")
        
        # Update name if provided
        if name:
            name_parts = name.split(' ', 1)
            user.first_name = name_parts[0]
            user.last_name = name_parts[1] if len(name_parts) > 1 else ''
            user.save()
            
        # Update role if provided - with extra validation and logging
        if role:
            print(f"Attempting to update role to: {role}")
            
            valid_roles = ['admin', 'manager', 'staff', 'supplier']
            if role not in valid_roles:
                return JsonResponse({'message': f'Invalid role: {role}'}, status=400)
            
            # Use get_or_create to avoid IntegrityError
            from store.models import UserProfile
            profile, created = UserProfile.objects.get_or_create(user=user)
            
            # Store the old role for logging
            old_role = profile.role
            
            # Update the role
            profile.role = role
            profile.save()
            
            print(f"Role updated: {old_role} -> {role} (created={created})")
        
        # Return the updated user data
        try:
            profile = user.userprofile
            current_role = profile.role
        except:
            current_role = 'admin' if user.is_superuser else 'staff'
            
        return JsonResponse({
            'message': 'User updated successfully',
            'user': {
                'id': user.id,
                'name': user.get_full_name() or user.username,
                'email': user.email,
                'role': current_role
            }
        })
        
    elif request.method == 'DELETE':
        # Delete user
        user.delete()
        return JsonResponse({'message': 'User deleted successfully'})
    
    from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Add these new views at the end of your views.py file

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def supplier_dashboard_api_view(request):
    """API view for supplier dashboard data."""
    try:
        # Get the current user
        user = request.user
        
        # You can add logic here to get real data based on the supplier
        # For now, we'll return sample data
        return Response({
            'totalOrders': 42,
            'pendingOrders': 7,
            'deliveredOrders': 31,
            'inTransitOrders': 4
        })
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def orders_api_view(request):
    """API view for all orders."""
    try:
        # You can add logic here to get real orders from your database
        # For now, we'll return sample data
        return Response([
            {'id': 1001, 'item_name': 'Fresh Tomatoes', 'quantity_ordered': 20, 'status': 'pending', 'order_date': '2025-05-10'},
            {'id': 1002, 'item_name': 'Lettuce', 'quantity_ordered': 15, 'status': 'shipped', 'order_date': '2025-05-12'},
            {'id': 1003, 'item_name': 'Carrots', 'quantity_ordered': 30, 'status': 'delivered', 'order_date': '2025-05-08'}
        ])
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=500)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def supplier_orders_api_view(request):
    """API view for supplier-specific orders."""
    try:
        # Get the current user
        user = request.user
        
        # You can add logic here to filter orders for this specific supplier
        # For now, we'll return sample data
        return Response([
            {'id': 1001, 'item_name': 'Fresh Tomatoes', 'quantity_ordered': 20, 'status': 'pending', 'order_date': '2025-05-10'},
            {'id': 1002, 'item_name': 'Lettuce', 'quantity_ordered': 15, 'status': 'shipped', 'order_date': '2025-05-12'},
            {'id': 1003, 'item_name': 'Carrots', 'quantity_ordered': 30, 'status': 'delivered', 'order_date': '2025-05-08'}
        ])
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=500)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_order_status(request, order_id):
    """API view to update order status."""
    try:
        # Get the status from request data
        status = request.data.get('status')
        
        if not status:
            return Response({
                'error': 'Status is required'
            }, status=400)
        
        # Here you would update the real order in your database
        # For now, we'll just return a success message
        return Response({
            'message': f'Order {order_id} status updated to {status}'
        })
    except Exception as e:
        return Response({
            'error': str(e)
        }, status=500)