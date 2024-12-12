import django_filters
from .models import ProductVariant

class ProductVariantFilter(django_filters.FilterSet):
    class Meta:
        model = ProductVariant
        fields = {
            'color' : ['icontains'],
            'size' : ['iexact','istartswith'],
            'product__name' : ['icontains'],
            'variant_price': ['exact','gt','lt'],
            'product__category__name' :['icontains']
        }


