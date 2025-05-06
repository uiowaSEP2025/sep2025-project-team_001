import pytest
from app.models.customer_models import CustomUser
from app.serializers.restaurant_serializer import RestaurantSerializer


@pytest.mark.django_db
def test_restaurant_serializer_serialization(restaurant):
    """
    RestaurantSerializer should correctly serialize a Restaurant instance.
    """
    serializer = RestaurantSerializer(restaurant)
    data = serializer.data

    # Basic fields
    assert data["id"] == restaurant.id
    assert data["name"] == restaurant.name
    assert data["address"] == restaurant.address
    assert data["phone"] == restaurant.phone

    # Field renamed to restaurant_image_url
    assert "restaurant_image_url" in data
    assert data["restaurant_image_url"] == restaurant.restaurant_image_url

    # User is represented by its ID
    assert data["user"] == restaurant.user.id


@pytest.mark.django_db
def test_restaurant_serializer_deserialization_valid():
    """
    Valid input data should deserialize into a Restaurant instance.
    """
    user = CustomUser.objects.create_user(
        username="owner",
        email="owner@example.com",
        password="testpass"
    )
    payload = {
        "user": user.pk,
        "name": "New Restaurant",
        "address": "456 New St",
        "phone": "123-456-7890",
        "restaurant_image_url": "http://example.com/new.png",
    }
    serializer = RestaurantSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors
    restaurant = serializer.save()

    assert restaurant.user == user
    assert restaurant.name == payload["name"]
    assert restaurant.address == payload["address"]
    assert restaurant.phone == payload["phone"]
    assert restaurant.restaurant_image_url is None


@pytest.mark.django_db
def test_restaurant_serializer_deserialization_invalid():
    """
    Missing required field (name) should cause validation failure.
    """
    user = CustomUser.objects.create_user(
        username="owner2",
        email="owner2@example.com",
        password="pass"
    )
    payload = {
        "user": user.pk,
        "address": "123 Missing Name St",
        "phone": "111-222-3333",
        "restaurant_image_url": "http://example.com/fake.png",
    }
    serializer = RestaurantSerializer(data=payload)
    assert not serializer.is_valid()
    assert "name" in serializer.errors
