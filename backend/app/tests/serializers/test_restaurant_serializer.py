import pytest

from app.serializers.restaurant_serializers import RestaurantSerializer


@pytest.mark.django_db
def test_restaurant_serializer_serialization(restaurant):
    """
    Test that the serializer correctly serializes a Restaurant instance.
    """
    serializer = RestaurantSerializer(restaurant)
    data = serializer.data
    # Check that the output contains expected fields.
    assert data["id"] == restaurant.id
    assert data["name"] == restaurant.name
    assert data["address"] == restaurant.address
    assert data["phone"] == restaurant.phone
    # Ensure that fields not specified in the serializer are omitted.
    assert "restaurant_image" not in data


@pytest.mark.django_db
def test_restaurant_serializer_deserialization_valid():
    """
    Test that valid input data passes validation and creates a Restaurant instance.
    """
    data = {
        "name": "New Restaurant",
        "address": "456 New St",
        "phone": "123-456-7890"
    }
    serializer = RestaurantSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    restaurant = serializer.save()
    assert restaurant.name == data["name"]
    assert restaurant.address == data["address"]
    assert restaurant.phone == data["phone"]


@pytest.mark.django_db
def test_restaurant_serializer_deserialization_invalid():
    """
    Test that invalid input data fails validation.
    Here, 'name' is required, so omitting it should result in an error.
    """
    data = {
        "address": "456 New St",
        "phone": "123-456-7890"
    }
    serializer = RestaurantSerializer(data=data)
    assert not serializer.is_valid()
    assert "name" in serializer.errors
