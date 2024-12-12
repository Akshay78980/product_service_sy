from products.models import Category,Brand, Product, ProductVariant
import pytest

from django.db import IntegrityError
from django.core.exceptions import ValidationError
from decimal import Decimal
from django.core.files.uploadedfile import SimpleUploadedFile

from django.db import transaction

# -----------------Tests for ProductVariant model------------------------


@pytest.mark.django_db
def test_product_variant_creation():
    """Test for creating a Productvariant"""
    category = Category.objects.create(name="Hoodie")
    brand = Brand.objects.create(name="Adidas")

    product1 = Product.objects.create(
        category = category,
        brand = brand,
        group_sku_number = "AD0001",
        name = "Adidas Plain Hoodie",
        description = "A perfect hoodie for men",
        price = Decimal('599.99')
    )

    image_file_1 = SimpleUploadedFile(
        name = "test_image.jpg",
        content = b"mock_file_content",
        content_type = "image/jpeg"
    )

    variant = ProductVariant.objects.create(
        product = product1,
        description = "Blue adidas plain hoodie perfect fit for men",
        color = "blue",
        size = "M",
        quantity = 20,
        variant_price = Decimal("799.99"),
        image1 = image_file_1
    )
    variant.full_clean()

    assert variant.product == product1
    assert variant.description == "Blue adidas plain hoodie perfect fit for men"
    assert variant.color == "#0000ff"
    assert variant.size == "M"
    assert variant.quantity == 20
    assert variant.variant_price == Decimal("799.99")
    assert variant.image1.name.startswith("product_images/test_image")
    assert ProductVariant.objects.count() == 1



@pytest.mark.django_db
def test_product_variant_valid_color_name():
    """Test product variant creation with valid color name"""

    category = Category.objects.create(name="Hoodie")
    brand = Brand.objects.create(name="Adidas")

    product1 = Product.objects.create(
        category = category,
        brand = brand,
        group_sku_number = "AD0001",
        name = "Adidas Plain Hoodie",
        description = "A perfect hoodie for men",
        price = Decimal('599.99')
    )

    image_file_1 = SimpleUploadedFile(
        name = "test_image.jpg",
        content = b"mock_file_content",
        content_type = "image/jpeg"
    )


    variant = ProductVariant.objects.create(
        product = product1,
        description = "Red adidas plain hoodie perfect fit for men",
        color = "blue",
        size = "S",
        quantity = 15,
        variant_price = Decimal("699.99"),
        image1 = image_file_1
    )
    variant.full_clean()
    assert variant.color == "#0000ff"




@pytest.mark.django_db
def test_product_variant_invalid_color_name():
    """Test product variant with invalid color name"""

    category = Category.objects.create(name="Hoodie")
    brand = Brand.objects.create(name="Adidas")

    product1 = Product.objects.create(
        category = category,
        brand = brand,
        group_sku_number = "AD0001",
        name = "Adidas Plain Hoodie",
        description = "A perfect hoodie for men",
        price = Decimal('599.99')
    )

    image_file_1 = SimpleUploadedFile(
        name = "test_image.jpg",
        content = b"mock_file_content",
        content_type = "image/jpeg"
    )

    with pytest.raises(ValidationError) as error_msg:
        variant = ProductVariant.objects.create(
            product = product1,
            description = "Blue adidas plain hoodie perfect fit for men",
            color = "blueesss",
            size = "M",
            quantity = 20,
            variant_price = Decimal("799.99"),
            image1 = image_file_1
        )
        variant.full_clean()
        assert "Invalid color format. Please provide a valid color name or hex code." in str(error_msg.value)




    

@pytest.mark.django_db
def test_product_variant_valid_hex_color_code():
    """Test product variant with valid hex color code"""

    category = Category.objects.create(name="Hoodie")
    brand = Brand.objects.create(name="Adidas")

    product1 = Product.objects.create(
        category = category,
        brand = brand,
        group_sku_number = "AD0001",
        name = "Adidas Plain Hoodie",
        description = "A perfect hoodie for men",
        price = Decimal('599.99')
    )

    image_file_1 = SimpleUploadedFile(
        name = "test_image.jpg",
        content = b"mock_file_content",
        content_type = "image/jpeg"
    )

    
    variant = ProductVariant.objects.create(
        product = product1,
        description = "Red adidas plain hoodie perfect fit for men",
        color = "#f00",
        size = "S",
        quantity = 15,
        variant_price = Decimal("699.99"),
        image1 = image_file_1
    )
    variant.full_clean()
    assert variant.color == "#ff0000"




@pytest.mark.django_db
def test_product_variant_invalid_hex_color_code():
    """Test product variant with invalid hex color code"""

    category = Category.objects.create(name="Hoodie")
    brand = Brand.objects.create(name="Adidas")

    product1 = Product.objects.create(
        category = category,
        brand = brand,
        group_sku_number = "AD0001",
        name = "Adidas Plain Hoodie",
        description = "A perfect hoodie for men",
        price = Decimal('599.99')
    )

    image_file_1 = SimpleUploadedFile(
        name = "test_image.jpg",
        content = b"mock_file_content",
        content_type = "image/jpeg"
    )

    with pytest.raises(ValidationError) as error_msg:
        variant = ProductVariant.objects.create(
            product = product1,
            description = "Green adidas plain hoodie perfect fit for men",
            color = "#GGG",
            size = "M",
            quantity = 13,
            variant_price = Decimal("799.99"),
            image1 = image_file_1
        )
        variant.full_clean()
        assert "Invalid color format. Please provide a valid color name or hex code." in str(error_msg.value)




@pytest.mark.django_db
def test_product_variant_unique_together():
    """Test that duplicate product variant (same product, color, and size) is not allowed"""

    category = Category.objects.create(name="Hoodie")
    brand = Brand.objects.create(name="Adidas")
    product1 = Product.objects.create(
        category=category,
        brand=brand,
        group_sku_number="AD0001",
        name="Adidas Plain Hoodie",
        description="A perfect hoodie for men",
        price=Decimal('599.99')
    )
    image_file_1 = SimpleUploadedFile(
        name="test_image.jpg",
        content=b"mock_file_content",
        content_type="image/jpeg"
    )
    
    ProductVariant.objects.create(
        product=product1,
        description="Red adidas plain hoodie perfect fit for men",
        color="#f00",
        size="S",
        quantity=15,
        variant_price=Decimal("699.99"),
        image1=image_file_1
    )
    
    # Catch IntegrityError when trying to create a duplicate variant
    with pytest.raises(IntegrityError):
        with transaction.atomic():  # Ensure the block is atomic and any errors will rollback
            ProductVariant.objects.create(
                product=product1,
                description="Another Red hoodie variant",
                color="#f00",
                size="S",
                quantity=20,
                variant_price=Decimal("799.99"),
                image1=image_file_1
            )

    # Check that the count is still 1 (only the first variant was created)
    assert ProductVariant.objects.count() == 1



@pytest.mark.django_db
def test_product_variant_empty_color():
    """Test product variant with empty or null color"""
    category = Category.objects.create(name="Hoodie")
    brand = Brand.objects.create(name="Adidas")
    product1 = Product.objects.create(
        category=category,
        brand=brand,
        group_sku_number="AD0001",
        name="Adidas Plain Hoodie",
        description="A perfect hoodie for men",
        price=Decimal('599.99')
    )
    image_file_1 = SimpleUploadedFile(
        name="test_image.jpg",
        content=b"mock_file_content",
        content_type="image/jpeg"
    )
    
    # Variant with empty color (null or blank)
    variant = ProductVariant.objects.create(
        product=product1,
        description="Hoodie without color",
        color=None,
        size="S",
        quantity=10,
        variant_price=Decimal("699.99"),
        image1=image_file_1
    )
    variant.full_clean()
    assert variant.color is None


@pytest.mark.django_db
def test_product_variant_multiple_images():
    """Test product variant with multiple images"""

    category = Category.objects.create(name="Hoodie")
    brand = Brand.objects.create(name="Adidas")
    product = Product.objects.create(
        category=category,
        brand=brand,
        group_sku_number="AD0001",
        name="Adidas Plain Hoodie",
        description="A perfect hoodie for men",
        price=Decimal('599.99')
    )

    image_file_1 = SimpleUploadedFile(
        name="test_image1.jpg",
        content=b"content of test_image1",
        content_type='image/jpeg'
    )

    image_file_3 = SimpleUploadedFile(
        name = 'test_image3.jpg',
        content = b'content of test_image3',
        content_type = "image/jpeg"
    )

    image_file_4 = SimpleUploadedFile(
        name = 'test_image4.jpg',
        content = b'content of test_image4',
        content_type = "image/jpeg"
    )

    variant = ProductVariant.objects.create(
        product = product,
        description = "A fit red Adidas plain Hoodie",
        color = 'red',
        size = 'M',
        quantity = 30,
        variant_price = Decimal('899.99'),
        image1 = image_file_1,
        image3 = image_file_3,
        image4 = image_file_4
    )

    assert variant.image1.name.startswith("product_images/test_image1")
    assert variant.image3.name.startswith("product_images/test_image3")
    assert variant.image4.name.startswith("product_images/test_image4")



@pytest.mark.django_db
def test_product_variant_invalid_size():
    """Test product variant with invalid size"""

    category = Category.objects.create(name="Hoodie")
    brand = Brand.objects.create(name="Adidas")
    product1 = Product.objects.create(
        category=category,
        brand=brand,
        group_sku_number="AD0001",
        name="Adidas Plain Hoodie",
        description="A perfect hoodie for men",
        price=Decimal('599.99')
    )
    image_file_1 = SimpleUploadedFile(
        name="test_image.jpg",
        content=b"mock_file_content",
        content_type="image/jpeg"
    )
    
    with pytest.raises(ValidationError):
        variant = ProductVariant(
            product=product1,
            description="Hoodie with invalid size",
            color="#f00",
            size="XXXXXXL",  # Invalid size, not in ('S', 'M', 'L', 'XL')
            quantity=10,
            variant_price=Decimal("699.99"),
            image1=image_file_1
        )
        variant.full_clean()
        


@pytest.mark.django_db
def test_product_variant_invalid_price():
    """Test product variant with invalid price"""

    category = Category.objects.create(name="Hoodie")
    brand = Brand.objects.create(name="Adidas")
    product1 = Product.objects.create(
        category=category,
        brand=brand,
        group_sku_number="AD0001",
        name="Adidas Plain Hoodie",
        description="A perfect hoodie for men",
        price=Decimal('599.99')
    )
    image_file_1 = SimpleUploadedFile(
        name="test_image.jpg",
        content=b"mock_file_content",
        content_type="image/jpeg"
    )
    
    with pytest.raises(ValidationError):
        variant = ProductVariant(
            product=product1,
            description="Hoodie with invalid price",
            color="#f00",
            size="S",
            quantity=10,
            variant_price=Decimal("-10.00"),  # Invalid negative price
            image1=image_file_1
        )
        variant.full_clean()



@pytest.mark.django_db
def test_product_variant_price_greater_than_or_equal_to_product_price():
    """Test whether the product variant price is 
        greater than or equal to base price of the product
    """

    category = Category.objects.create(name="Hoodie")
    brand = Brand.objects.create(name="Adidas")
    product = Product.objects.create(
        category=category,
        brand=brand,
        group_sku_number="AD0001",
        name="Adidas Plain Hoodie",
        description="A perfect hoodie for men",
        price=Decimal('599.99')
    )
    image_file_1 = SimpleUploadedFile(
        name="test_image.jpg",
        content=b"mock_file_content",
        content_type="image/jpeg"
    )

    with pytest.raises(ValidationError):
        variant = ProductVariant(
            product=product,
            description="A red perfect adidas Hoodie",
            color="red",
            size="S",
            quantity=10,
            variant_price=Decimal("399.00"),
            image1=image_file_1
        )
        variant.full_clean()
        variant.save()
    
    assert ProductVariant.objects.count() == 0