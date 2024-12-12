import pytest
from decimal import Decimal
from products.models import Product, Category, Brand, ProductVariant
from products.serializers import ProductVariantSerializer
from django.core.files.uploadedfile import SimpleUploadedFile

from PIL import Image
import io


def generate_mock_image():
    """Generate a valid mock image file."""
    image = Image.new("RGB", (100, 100), color="blue")
    image_io = io.BytesIO()
    image.save(image_io, format="JPEG")
    image_io.seek(0)
    return SimpleUploadedFile("test_image.jpg", image_io.read(), content_type="image/jpeg")



@pytest.mark.django_db
class TestProductVariantSerializer:

    @pytest.fixture
    def setup_data(self):
        """Fixture to set up initial data."""
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
        return product


    def test_valid_data(self, setup_data):
        """Test serializer with valid data."""
        product = setup_data
        image_file = generate_mock_image()

        data = {
            "product_id": product.product_id,
            "description": "Red adidas hoodie",
            "color": "#FF5733",
            "size": "M",
            "quantity": 10,
            "variant_price": "699.99",
            "image1": image_file,
        }

        serializer = ProductVariantSerializer(data=data)
        assert serializer.is_valid()


    def test_missing_required_fields(self):
        """Test serializer with missing required fields."""
        data = {}
        serializer = ProductVariantSerializer(data=data)
        assert not serializer.is_valid()
        assert "product_id" in serializer.errors
        assert "quantity" in serializer.errors
        assert "color" in serializer.errors
        assert "size" in serializer.errors
        assert "image1" in serializer.errors



    def test_invalid_product_id(self):
        """Test serializer with invalid product_id."""
        data = {
            "product_id": 999,  # Non-existent product ID
            "description": "Invalid product test",
            "color": "#FF5733",
            "size": "M",
            "quantity": 10,
            "variant_price": "699.99",
        }
        serializer = ProductVariantSerializer(data=data)
        assert not serializer.is_valid()
        assert "product_id" in serializer.errors



    def test_read_only_product_field(self, setup_data):
        """Test read-only product field."""
        product = setup_data
        variant = ProductVariant.objects.create(
            product=product,
            description="A variant description",
            color="#FF5733",
            size="M",
            quantity=10,
            variant_price=Decimal("699.99"),
            image1=SimpleUploadedFile(
                name="test_image.jpg",
                content=b"mock_file_content",
                content_type="image/jpeg"
            ),
        )
        serializer = ProductVariantSerializer(instance=variant)
        data = serializer.data
        assert "product" in data
        assert str(data["product"]["product_id"]) == str(product.product_id)
        assert "product_id" not in data  # Ensure write-only field is not in output



    
    def test_write_only_product_id_field(self, setup_data):
        """Test write-only product_id field."""
        product = setup_data
        image_file = generate_mock_image()  # Use the valid mock image generator
        data = {
            "product_id": product.product_id,
            "description": "Write-only test",
            "color": "#FF5733",
            "size": "L",
            "quantity": 15,
            "variant_price": "799.99",
            "image1": image_file,
        }
        serializer = ProductVariantSerializer(data=data)
        assert serializer.is_valid()
        # instance = serializer.save()
        # assert instance.product == product
        # serializer = ProductVariantSerializer(instance=instance)
        # serialized_data = serializer.data
        # assert "product_id" not in serialized_data  # Ensure write-only field is not in output