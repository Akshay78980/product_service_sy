from products.models import Category,Brand, Product
import pytest

from django.core.exceptions import ValidationError
from decimal import Decimal


# -----------------Tests for Brand model------------------------


@pytest.mark.django_db
def test_brand_creation():
    '''Test brand can be created successfully'''

    brand = Brand.objects.create(name="Adidas")
    assert Brand.objects.count() == 1
    assert brand.name == "Adidas"


@pytest.mark.django_db
def test_case_insensitive_unique_brand():
    """Test the brands are case-insensitively unique"""

    brand = Brand.objects.create(name="Adidas")
    with pytest.raises(ValidationError):
        Brand.objects.create(name="adidas")

    with pytest.raises(ValidationError):
        Brand.objects.create(name="aDidas")

    brand = Brand.objects.create(name="Alen Solly")

    assert Brand.objects.count() == 2


@pytest.mark.django_db
def test_cascade_delete_brand():
    """Test that deleting a Brand cascades deletes associated Products."""
    category = Category.objects.create(name="Footwear")
    brand = Brand.objects.create(name="Puma")
    product = Product.objects.create(
        category=category,
        brand=brand,
        group_sku_number="SKU77777",
        name="Sandals",
        price=Decimal("49.99")
    )

    brand.delete()

    assert not Product.objects.filter(pk=product.pk).exists()