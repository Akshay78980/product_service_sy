from django.urls import path
from .views import ProductListView, ProductView

urlpatterns = [
    path('product/', ProductListView.as_view(), name='product_list'),
    path('product/<int:pk>/', ProductView.as_view(), name='product_view'),
]