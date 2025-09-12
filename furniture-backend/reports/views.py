# reports/views.py
from rest_framework import viewsets, permissions
from .models import SalesReport, InventoryReport
from .serializers import SalesReportSerializer, InventoryReportSerializer

class SalesReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SalesReport.objects.all().order_by('-date')
    serializer_class = SalesReportSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admin can view

class InventoryReportViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = InventoryReport.objects.all().order_by('-date')
    serializer_class = InventoryReportSerializer
    permission_classes = [permissions.IsAdminUser]  # Only admin can view
