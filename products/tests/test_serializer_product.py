import pytest
from decimal import Decimal
from products.models import Category, Brand
from products.serializers import ProductSerializer



@pytest.mark.django_db
def test_product_serializer_valid_data():
    category = Category.objects.create(name="Hoodie")
    brand = Brand.objects.create(name="Adidas")
    data = {
        'category': category.id,
        'brand': brand.id,
        'group_sku_number': 'AD001',
        'name': 'Adidas Hoodie',
        'description': 'A comfortable hoodie',
        'price': Decimal('599.99')
    }
    serializer = ProductSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    product = serializer.save()
    assert product.name == 'Adidas Hoodie'
    assert product.price == Decimal('599.99')



@pytest.mark.django_db
def test_product_serializer_invalid_data():
    data = {
        'category': None,
        'brand': None,
        'group_sku_number': '',
        'name': '',
        'description': ''
    }
    serializer = ProductSerializer(data=data)
    assert not serializer.is_valid()
    assert 'price' in serializer.errors
    assert 'group_sku_number' in serializer.errors
    assert 'category' in serializer.errors
    assert 'brand' in serializer.errors
