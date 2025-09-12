from django.contrib import admin
from .models import Promotion, Coupon


@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('name', 'promo_type', 'value', 'active', 'start_date', 'end_date')
    list_filter = ('promo_type', 'active', 'start_date')
    search_fields = ('name', 'description')
    filter_horizontal = ('products', 'categories')


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ('code', 'discount_type', 'value', 'active', 'used_count', 'usage_limit', 'start_date', 'end_date')
    list_filter = ('discount_type', 'active', 'start_date')
    search_fields = ('code', 'description')
