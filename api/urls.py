from django.urls import path, include
from products.views import GetAvailableSizesAPI

from products.views import BrandViewSet,CategoryViewSet, ProductViewSet, ProductVariantViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('category',CategoryViewSet)
router.register('brand',BrandViewSet)
router.register('product',ProductViewSet)
router.register('product-variant',ProductVariantViewSet)

urlpatterns = [
    path('product-sizes/<str:group_sku_number>/<str:product_color>/',GetAvailableSizesAPI.as_view(), name="get_available_sizes"),
    path("",include(router.urls)),
]