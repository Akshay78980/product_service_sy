from products.models import Category,Brand, Product
import pytest

from django.db import IntegrityError
from decimal import Decimal


# -----------------Tests for Product model------------------------


@pytest.mark.django_db
def test_product_creation():
    """Test product can be created successfully"""

    category = Category.objects.create(name="Hoodie")
    brand = Brand.objects.create(name="LP")
    product = Product.objects.create(
        category=category,
        brand=brand,
        group_sku_number="LP0001",
        name="Louis Philipe Plain Hoodie",
        description="A stylish hoodie perfect fit for men",
        price=Decimal("599.99")
    )
    assert product.category == category
    assert product.brand == brand
    assert product.group_sku_number == "LP0001"
    assert product.name == "Louis Philipe Plain Hoodie"
    assert product.description == "A stylish hoodie perfect fit for men"
    assert product.price == Decimal("599.99")
    assert Product.objects.count() == 1



@pytest.mark.django_db
def test_product_update():
    """Test updating a Product object."""
    category = Category.objects.create(name="Electronics")
    brand = Brand.objects.create(name="Apple")
    product = Product.objects.create(
        category=category,
        brand=brand,
        group_sku_number="SKU54321",
        name="iPhone 14",
        description="Latest iPhone model",
        price=Decimal("1099.99")
    )

    product.name = "iPhone 14 Pro"
    product.price = Decimal("1299.99")
    product.save()

    updated_product = Product.objects.get(group_sku_number="SKU54321")
    assert updated_product.name == "iPhone 14 Pro"
    assert updated_product.price == Decimal("1299.99")




@pytest.mark.django_db
def test_product_deletion():
    """Test deleting a Product object."""
    category = Category.objects.create(name="Footwear")
    brand = Brand.objects.create(name="Puma")
    product = Product.objects.create(
        category=category,
        brand=brand,
        group_sku_number="SKU77777",
        name="Sandals",
        price=Decimal("49.99")
    )
    product.delete()

    assert Product.objects.filter(group_sku_number="SKU77777").count() == 0




@pytest.mark.django_db
def test_product_str_representation():
    """Test product string representation is correct"""

    category = Category.objects.create(name="T-shirt")
    brand = Brand.objects.create(name="Adidas")
    product = Product.objects.create(
        category=category,
        brand=brand,
        group_sku_number="AD0001",
        name="Adidas Plain T-Shirt",
        description="A perfect fit for men",
        price=Decimal("799.50")
    )

    assert str(product) == "Adidas Plain T-Shirt (AD0001)"


@pytest.mark.django_db
def test_product_blank_description():
    """Test creating product with blank description"""

    category = Category.objects.create(name="T-shirt")
    brand = Brand.objects.create(name="Allen Solly")
    product = Product.objects.create(
        category=category,
        brand=brand,
        group_sku_number="AD0001",
        name="Allen Solly Plain T-Shirt",
        price=Decimal("1000.89")
    )

    product.description == ""


@pytest.mark.django_db
def test_product_group_sku_number_unique():
    """Test the group sku number for product is unique"""

    category = Category.objects.create(name="T-shirt")
    brand = Brand.objects.create(name="Allen Solly")
    product1 = Product.objects.create(
        category=category,
        brand=brand,
        group_sku_number="AD0001",
        name="Allen Solly Plain T-Shirt",
        description="A great t shirt",
        price=Decimal("1000.89")
    )

    with pytest.raises(IntegrityError):
        product2 = Product.objects.create(
            category=category,
            brand=brand,
            group_sku_number="AD0001",
            name="Allen Solly Printed T-Shirt",
            description="A great printed t-shirt",
            price=Decimal("1000.89")
        )



@pytest.mark.django_db
def test_product_index_query_by_name():
    """Test querying a product by name using the indexed field."""
    category = Category.objects.create(name="Gaming")
    brand = Brand.objects.create(name="Sony")
    product = Product.objects.create(
        category=category,
        brand=brand,
        group_sku_number="SKU11111",
        name="PlayStation 5",
        price=Decimal("499.99")
    )

    result = Product.objects.filter(name="PlayStation 5")

    assert result.exists()
    assert result.first() == product
    assert Product.objects.count() == 1