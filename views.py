from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
import csv
from django.http import HttpResponse
from UserRoles import InventoryItem, Supplier, Order, Notification


def is_admin(user):
    return user.groups.filter(name="Admin").exists()

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    stock_reports = StockReport.objects.order_by('-created_at').first()
    order_summary = OrderSummary.Objects.order_by('-created_at').first()
    suppliers = SuppliersPerformance.objects.all()

    return render(request, 'admin/dashboard.html', {
        'stock_reports': stock_reports, 
        'order_summary': order_summary,
        'suppliers': suppliers, 
    })

@login_required
@user_passes_test(is_admin)
def manage_users(request):
    users = User.objects.all()
    return render(request, 'admin/manage_users.html', {'users': users})

@login_required
@user_passes_test(is_admin)
def export_stock_report_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="stock_report.csv"'

    writer = csv.writer(response)
    writer.writerow(['Date', 'Total Items', 'Low Stock Items', 'Expired Items'])

    reports = StockReport.objects.all()
    for report in reports:
        writer.writerow([report.created_at, report.total_items, report.low_stock_items, report.expired_items])

    return response

# Function to Assign User to a Role Group
def assign_user_to_group(user, role):
    role = role.lower()
    group_name = None

    if role == "admin":
        group_name = "Admin"
    elif role == "manager":
        group_name = "Manager"
    elif role == "staff":
        group_name = "Staff"

    if group_name:
        group, created = Group.objects.get_or_create(name=group_name)
        user.groups.add(group)
        user.save()

# Inventory Dashboard - Shows stock levels, expiry alerts
@login_required
def inventory_dashboard(request):
    items = InventoryItem.objects.all()
    low_stock_items = [item for item in items if item.is_low_stock()]
    expired_items = [item for item in items if item.is_expired()]
    notifications = Notification.objects.filter(is_read=False)

    return render(request, 'inventory/dashboard.html', {
        'items': items,
        'low_stock_items': low_stock_items,
        'expired_items': expired_items,
        'notifications': notifications
    })

# Create a New Order (Only Admin & Managers)
@login_required
def create_order(request):
    role = request.user.profile.role if hasattr(request.user, 'profile') else None
    if role not in ['Admin', 'Manager']:
        return redirect('inventory_dashboard')

    suppliers = Supplier.objects.all()
    if request.method == 'POST':
        supplier_id = request.POST.get('supplier')
        supplier = get_object_or_404(Supplier, id=supplier_id)
        order = Order.objects.create(supplier=supplier, created_by=request.user)

        return redirect('order_list')

    return render(request, 'inventory/create_order.html', {'suppliers': suppliers})

# View All Orders
@login_required
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'inventory/orders.html', {'orders': orders})

# Update Stock Levels (Staff only)
@login_required
def update_stock(request, item_id):
    item = get_object_or_404(InventoryItem, id=item_id)

    if request.method == 'POST':
        new_quantity = int(request.POST.get('quantity'))
        item.quantity = new_quantity
        item.save()
        return redirect('inventory_dashboard')

    return render(request, 'inventory/update_stock.html', {'item': item})
