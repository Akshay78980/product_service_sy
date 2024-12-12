from decimal import Decimal
import pytest
from rest_framework import status
from rest_framework.test import APIClient
from products.models import Category, Brand, Product, ProductVariant



@pytest.mark.django_db
class TestProductVariantViewSet:

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
            price="599.99"
        )
        product_variant = ProductVariant.objects.create(
            product=product,
            description="Red adidas hoodie",
            color="#FF5733",
            size="M",
            quantity=10,
            variant_price="699.99"
        )
        return product_variant



    def test_get_product_variant_view(self, setup_data):
        """Test GET request to retrieve all product variants."""
        client = APIClient()
        response = client.get('/api/product-variant/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
        assert response.data['results'][0]['description'] == setup_data.description



    # def test_post_product_variant_view(self):
    #     """Test POST request to create a new product variant."""
    #     client = APIClient()
    #     data = {
    #         "product_id": 1,  # Assuming this ID is valid
    #         "description": "Blue Adidas Hoodie",
    #         "color": "#0000FF",
    #         "size": "L",
    #         "quantity": 5,
    #         "variant_price": Decimal("799.99")
    #     }
    #     response = client.post('/api/product-variant/', data, format='json')
    #     assert response.status_code == status.HTTP_201_CREATED
    #     assert response.data['description'] == data['description']



    # def test_put_product_variant_view(self, setup_data):
    #     """Test PUT request to update an existing product variant."""
    #     client = APIClient()
    #     data = {
    #         "product_id": 1,  # Assuming this ID is valid
    #         "description": "Updated Red Adidas Hoodie",
    #         "color": "#FF5733",
    #         "size": "M",
    #         "quantity": 10,
    #         "variant_price": "799.99"
    #     }
    #     response = client.put(f'/api/product-variant/{setup_data.id}/', data, format='json')
    #     assert response.status_code == status.HTTP_200_OK
    #     assert response.data['description'] == data['description']




    # def test_delete_product_variant_view(self, setup_data):
    #     """Test DELETE request to delete a product variant."""
    #     client = APIClient()
    #     response = client.delete(f'/api/product-variant/{setup_data.id}/')
    #     assert response.status_code == status.HTTP_204_NO_CONTENT
    #     # Ensure product variant is deleted
    #     response = client.get('/api/product-variant/')
    #     assert len(response.data) == 0
