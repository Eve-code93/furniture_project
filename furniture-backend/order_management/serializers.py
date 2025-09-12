from rest_framework import serializers
from .models import Order, OrderItem, OrderStatusHistory
from products.serializers import ProductSerializer, ProductVariantSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    variant = ProductVariantSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = [
            'id', 'product', 'variant', 'quantity',
            'unit_price', 'total_price', 'created_at'
        ]


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusHistory
        fields = ['status', 'timestamp', 'note']


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'customer', 'status', 'total_price', 'shipping_cost',
            'discount_amount', 'shipping_address', 'delivery_instructions',
            'notes', 'created_at', 'updated_at', 'items', 'status_history'
        ]
        read_only_fields = ['total_price', 'created_at', 'updated_at']
