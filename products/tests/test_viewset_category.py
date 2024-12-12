import pytest
from rest_framework import status
from rest_framework.test import APIClient
from products.models import Category



@pytest.mark.django_db
class TestCategoryViewSet:

    @pytest.fixture
    def setup_data(self):
        """Fixture to set up initial data."""
        category = Category.objects.create(name="Hoodie")
        return category



    def test_get_category_api(self, setup_data):
        """Test GET request to retrieve all categories."""
        client = APIClient()
        response = client.get('/api/category/')
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['name'] == setup_data.name



    def test_post_category_api(self):
        """Test POST request to create a new category."""
        client = APIClient()
        data = {"name": "Jackets"}
        response = client.post('/api/category/', data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['name'] == data['name']



    def test_put_category_api(self, setup_data):
        """Test PUT request to update an existing category."""
        client = APIClient()
        data = {"name": "Updated Hoodie"}
        response = client.put(f'/api/category/{setup_data.id}/', data, format='json')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['name'] == data['name']



    def test_delete_category_view(self, setup_data):
        """Test DELETE request to delete a category."""
        client = APIClient()
        response = client.delete(f'/api/category/{setup_data.id}/')
        assert response.status_code == status.HTTP_204_NO_CONTENT
        
        response = client.get('/api/category/')
        assert len(response.data) == 0
