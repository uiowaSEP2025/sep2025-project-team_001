import pytest

from app.serializers.restaurant_serializers import RestaurantSerializer


@pytest.mark.django_db
def test_restaurant_serializer(restaurant):
    serializer = RestaurantSerializer(restaurant)
    data = serializer.data
    assert "id" in data
    assert data["name"] == "Testaurant"
    assert data["address"] == "123 Main St"
    assert data["phone"] == "555-555-5555"
    assert "restaurant_image" not in data
