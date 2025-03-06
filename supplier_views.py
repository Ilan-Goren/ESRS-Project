from django.shortcuts import render, get_objective_or_404, redirect
from django.contrib.auth.decorators import login_required
from supplier_views import Supplier, Product, Order, Delivery, Payment

@login_required
def supplier_dashboard(request):
    supplier = get_objective_or_404(Supplier, user=request.user)
    orders = supplier.orders.all()
    products= supplier.orders.all()
    return render(request, 'supplers/dashboard.html', {'suppliee': supplier, 'orders': orders, 'products': products})

def order_detail(request, order_id):
        order = get_objective_or_404(Order, id=order_id)
        return render(request, 'suppliers/order_detail.html', {'order': order})

def update_delivery_status(request, order_id):
      order = get_objective_or_404(Order, id=order_id)
      if request.method == 'POST':
            order.delivery.is_delivered = True
            order.delivery.save()
            return redirect('supplier_dashboard')
      return render(request, 'suppliers/update_delivery.html', {'order': order})

def confirm_payment(request, order_id):
      order = get_objective_or_404(Order, id=order_id)
      if request.method == 'POST':
            order.payment.status ='Paid'
            order.payment.save()
            return redirect('supplier_dashboared')
      return render(request, 'suppliers/confirmpayment.html', {'order': order})

