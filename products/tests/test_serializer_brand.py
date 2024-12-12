import pytest
from products.serializers import BrandSerializer



@pytest.mark.django_db
def test_brand_serializer_valid_data():
    data = {'name': 'Adidas'}
    serializer = BrandSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    brand = serializer.save()
    assert brand.name == 'Adidas'

@pytest.mark.django_db
def test_brand_serializer_invalid_data():
    data = {'name': ''}
    serializer = BrandSerializer(data=data)
    assert not serializer.is_valid()
    assert 'name' in serializer.errors