from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet, OrderItemViewSet, OrderStatusHistoryViewSet

router = DefaultRouter()
router.register(r'orders', OrderViewSet, basename='order')
router.register(r'order-items', OrderItemViewSet, basename='order-item')
router.register(r'order-status-history', OrderStatusHistoryViewSet, basename='order-status-history')

urlpatterns = [
    path('', include(router.urls)),
]
