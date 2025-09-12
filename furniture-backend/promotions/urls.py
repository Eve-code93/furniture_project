from rest_framework.routers import DefaultRouter
from .views import PromotionViewSet, CouponViewSet

router = DefaultRouter()
router.register('promotions', PromotionViewSet)
router.register('coupons', CouponViewSet)

urlpatterns = router.urls
