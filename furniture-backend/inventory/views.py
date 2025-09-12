from rest_framework import viewsets, permissions
from .models import Inventory
from .serializers import InventorySerializer


class InventoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Inventory.objects.all().select_related('product', 'category')
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated]
