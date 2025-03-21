from django.urls import path
from .api_views import (
    InventoryListCreateView,
    InventoryDetailView,
    OrderListCreateView,
    OrderDetailView,
    SupplierListCreateView,
    SupplierDetailView,
    TransactionListCreateView,
    TransactionDetailView,
    UserListCreateView,
    UserDetailView
)
from rest_framework.routers import DefaultRouter
from .api_views import OrderViewSet

urlpatterns = [
    # Inventory endpoints
    path('inventory/', InventoryListCreateView.as_view(), name='inventory-list-create'),
    path('inventory/<int:pk>/', InventoryDetailView.as_view(), name='inventory-detail'),

    # Orders endpoints
    path('orders/', OrderListCreateView.as_view(), name='order-list-create'),
    path('orders/<int:pk>/', OrderDetailView.as_view(), name='order-detail'),

    # Suppliers endpoints
    path('suppliers/', SupplierListCreateView.as_view(), name='supplier-list-create'),
    path('suppliers/<int:pk>/', SupplierDetailView.as_view(), name='supplier-detail'),

    # Transactions endpoints
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list-create'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),

    # Users endpoints
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]

router = DefaultRouter()
router.register(r'orders-viewset', OrderViewSet, basename='order-viewset')

urlpatterns += router.urls