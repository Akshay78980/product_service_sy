from products.models import Category,Brand, Product
import pytest

from django.core.exceptions import ValidationError
from decimal import Decimal


# -----------------Tests for Category model------------------------

@pytest.mark.django_db
def test_category_creation():
    '''Test the category can be created successfully'''

    category = Category.objects.create(name="Hoodie")
    assert category.name == "Hoodie"
    assert Category.objects.count() == 1



@pytest.mark.django_db
def test_case_insensitive_unique_category():
    """Test the category name is unique case-insensitively"""

    Category.objects.create(name="T-shirt")
    with pytest.raises(ValidationError):
        Category.objects.create(name="t-shirt")

    with pytest.raises(ValidationError):
        Category.objects.create(name="t-sHirt")

    with pytest.raises(ValidationError):
        Category.objects.create(name="t-shirts")

    Category.objects.create(name="Hoodie")



@pytest.mark.django_db
def test_cascade_delete_category():
    """Test that deleting a Category cascades deletes associated Products."""
    category = Category.objects.create(name="Footwear")
    brand = Brand.objects.create(name="Puma")
    product = Product.objects.create(
        category=category,
        brand=brand,
        group_sku_number="SKU77777",
        name="Sandals",
        price=Decimal("49.99")
    )

    category.delete()

    assert not Product.objects.filter(pk=product.pk).exists()
