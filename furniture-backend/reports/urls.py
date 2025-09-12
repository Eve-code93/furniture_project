# reports/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import SalesReportViewSet, InventoryReportViewSet

router = DefaultRouter()
router.register(r'sales', SalesReportViewSet, basename='sales-report')
router.register(r'inventory', InventoryReportViewSet, basename='inventory-report')

urlpatterns = [
    path('api/', include(router.urls)),
]
