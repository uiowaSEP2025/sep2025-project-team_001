import pytest
from app.models.customer_models import CustomUser
from app.serializers.restaurant_serializer import RestaurantSerializer


@pytest.mark.django_db
def test_restaurant_serializer_serialization(restaurant):
    """
    RestaurantSerializer should correctly serialize a restaurant instance.
    """
    serializer = RestaurantSerializer(restaurant)
    data = serializer.data
    assert data["id"] == restaurant.id
    assert data["name"] == restaurant.name
    assert data["address"] == restaurant.address
    assert data["phone"] == restaurant.phone
    assert data["restaurant_image"] == restaurant.restaurant_image
    assert data["user"] == restaurant.user.id


@pytest.mark.django_db
def test_restaurant_serializer_deserialization_valid():
    """
    Valid input data should deserialize into a Restaurant instance.
    """
    user = CustomUser.objects.create_user(username="owner", email="owner@example.com", password="testpass")
    data = {
        "user": user.pk,
        "name": "New Restaurant",
        "address": "456 New St",
        "phone": "123-456-7890",
        "restaurant_image": "base64string",
    }
    serializer = RestaurantSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    restaurant = serializer.save()
    assert restaurant.user == user
    assert restaurant.name == data["name"]
    assert restaurant.address == data["address"]
    assert restaurant.phone == data["phone"]
    assert restaurant.restaurant_image == data["restaurant_image"]


@pytest.mark.django_db
def test_restaurant_serializer_deserialization_invalid():
    """
    Missing required field (name) should cause validation failure.
    """
    user = CustomUser.objects.create_user(username="owner2", email="owner2@example.com", password="pass")
    data = {
        "user": user.pk,
        "address": "123 Missing Name St",
        "phone": "111-222-3333",
        "restaurant_image": "fakeimg",
    }
    serializer = RestaurantSerializer(data=data)
    assert not serializer.is_valid()
    assert "name" in serializer.errors
