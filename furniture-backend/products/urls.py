from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, FabricViewSet, ProductViewSet

router = DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('fabrics', FabricViewSet)
router.register('products', ProductViewSet)

urlpatterns = router.urls
