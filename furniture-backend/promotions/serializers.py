from rest_framework import serializers
from .models import Promotion, Coupon
from products.serializers import ProductSerializer, CategorySerializer


class PromotionSerializer(serializers.ModelSerializer):
    products = ProductSerializer(many=True, read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    is_active_now = serializers.ReadOnlyField()

    class Meta:
        model = Promotion
        fields = ['id', 'name', 'description', 'promo_type', 'value', 'active', 
                  'start_date', 'end_date', 'products', 'categories', 'is_active_now']


class CouponSerializer(serializers.ModelSerializer):
    can_use = serializers.ReadOnlyField()

    class Meta:
        model = Coupon
        fields = ['id', 'code', 'description', 'discount_type', 'value', 
                  'active', 'usage_limit', 'used_count', 'start_date', 'end_date', 'can_use']
