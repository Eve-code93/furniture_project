from rest_framework import serializers
from .models import Inventory
from products.serializers import ProductSerializer


class InventorySerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = Inventory
        fields = ['id', 'product', 'category', 'total_stock', 'sold', 'remaining', 'reorder_threshold', 'updated_at']
