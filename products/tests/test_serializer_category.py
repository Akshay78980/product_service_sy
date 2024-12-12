import pytest
from products.models import Category
from products.serializers import CategorySerializer
from rest_framework.exceptions import ValidationError as SerializerValidationError 



@pytest.mark.django_db
def test_category_serializer_valid_data():
    data = {
        'name': 'T-Shirt'
    }
    serializer = CategorySerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    category = serializer.save()
    assert category.name == 'T-Shirt'


@pytest.mark.django_db
def test_category_serializer_invalid_data():
    data = {'name': ''}
    serializer = CategorySerializer(data=data)
    assert not serializer.is_valid()
    assert 'name' in serializer.errors


