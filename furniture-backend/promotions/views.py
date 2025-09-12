from rest_framework import viewsets, permissions, filters
from .models import Promotion, Coupon
from .serializers import PromotionSerializer, CouponSerializer
from django_filters.rest_framework import DjangoFilterBackend


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission: Read-only for non-admins, full access for admins.
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all().prefetch_related('products', 'categories')
    serializer_class = PromotionSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['active', 'promo_type', 'start_date', 'end_date']
    search_fields = ['name', 'description']
    ordering_fields = ['start_date', 'end_date', 'value']
    ordering = ['-start_date']


class CouponViewSet(viewsets.ModelViewSet):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['active', 'discount_type', 'start_date', 'end_date']
    search_fields = ['code', 'description']
    ordering_fields = ['start_date', 'end_date', 'value']
    ordering = ['-start_date']
