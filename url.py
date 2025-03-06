from django.urls import path
from supplier_views import views

urlpatterns = [
    path('dashboard/', views.supplier_dashboard, name='supplier_dashboard'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('order/<int:order_id>/delivery/', views.update_delivery_status, name='update_delivery_status'),
    path('order/<int:order_id>/payment/', views.confirm_payment, name='confirm_payment'),
]
