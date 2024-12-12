from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.views import APIView

from .models import Brand, Category, Product, ProductVariant
from .serializers import CategorySerializer, ProductSerializer, ProductVariantSerializer, BrandSerializer

from rest_framework.response import Response

from django.views.generic import TemplateView

from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from .filters import ProductVariantFilter
# Create your views here.


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ProductVariantPagination(PageNumberPagination):
    page_size = 5
    max_page_size = 20
    page_size_query_param = 'page_size'


class ProductVariantViewSet(viewsets.ModelViewSet):
    queryset = ProductVariant.objects.all().distinct('product','color')
    serializer_class = ProductVariantSerializer
    pagination_class = ProductVariantPagination
    filterset_class = ProductVariantFilter
    search_fields = ['product__group_sku_number']
    

class GetAvailableSizesAPI(APIView):
    def get(self, request,group_sku_number,product_color):
        size_order = ['XS','S','M','L','XL','XXL','XXXL']
        data = ProductVariant.objects.filter(product__group_sku_number=group_sku_number,color=product_color).values('size', 'id').distinct()
        data_list = list(data)
        sorted_data_list = sorted(data_list,key=lambda dict_el: size_order.index(dict_el['size']),reverse=False)
        return Response(sorted_data_list)


class ProductListView(TemplateView):
    template_name = 'product_list.html'

class ProductView(TemplateView):
    template_name = 'product_view.html'



    

