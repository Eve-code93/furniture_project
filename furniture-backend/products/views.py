from rest_framework import viewsets, permissions, filters
from django_filters.rest_framework import DjangoFilterBackend
from .models import Category, Fabric, Product
from .serializers import CategorySerializer, FabricSerializer, ProductSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    Custom permission: Allow read-only access for everyone,
    but write access only to admin (staff) users.
    """
    def has_permission(self, request, view):
        # SAFE_METHODS are GET, HEAD, OPTIONS
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user and request.user.is_staff


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name', 'slug']


class FabricViewSet(viewsets.ModelViewSet):
    queryset = Fabric.objects.filter(is_active=True)
    serializer_class = FabricSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [filters.SearchFilter]
    search_fields = ['name']


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(
        is_active=True, show_in_catalog=True
    ).prefetch_related('images', 'variants')
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = [
        'category', 'color_family', 'style',
        'is_featured', 'is_bestseller', 'is_new_arrival',
        'supports_customization'
    ]
    search_fields = ['name', 'slug', 'description', 'short_description']
    ordering_fields = ['base_price', 'sale_price', 'created_at']
    ordering = ['-created_at']
    lookup_field = 'slug'
