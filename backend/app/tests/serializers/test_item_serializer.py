from decimal import Decimal

import pytest

from app.models.restaurant_models import Item
from app.serializers.item_serializer import ItemSerializer


@pytest.mark.django_db
def test_item_serializer_representation(restaurant):
    """
    Ensure that the serializer correctly serializes an Item instance.
    """
    item_instance = Item.objects.create(
        restaurant=restaurant,
        name="Test Burger",
        description="Delicious test burger",
        price=Decimal("9.99"),
        category="Food",
        stock=100,
        available=True,
        base64_image="dummybase64string"
    )
    serializer = ItemSerializer(item_instance)
    data = serializer.data
    assert data["id"] == item_instance.id
    assert data["name"] == "Test Burger"
    assert data["description"] == "Delicious test burger"
    assert data["price"] == Decimal("9.99")
    assert data["category"] == "Food"
    assert data["stock"] == 100
    assert data["available"] is True
    assert data["base64_image"] == "dummybase64string"
    assert data["restaurant"] == restaurant.id


@pytest.mark.django_db
def test_item_serializer_deserialization_valid(restaurant):
    """
    Test that valid input data is correctly validated and an Item instance is created.
    """
    data = {
        "restaurant": restaurant.pk,
        "name": "Test Sandwich",
        "description": "A tasty sandwich",
        "price": "5.99",
        "category": "Food",
        "stock": 50,
        "available": True,
        "base64_image": "somedummystring"
    }
    serializer = ItemSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    item_instance = serializer.save()
    assert item_instance.name == "Test Sandwich"
    assert item_instance.description == "A tasty sandwich"
    assert item_instance.price == Decimal("5.99")
    assert item_instance.category == "Food"
    assert item_instance.stock == 50
    assert item_instance.available is True
    assert item_instance.base64_image == "somedummystring"
    assert item_instance.restaurant == restaurant


@pytest.mark.django_db
def test_item_serializer_deserialization_invalid(restaurant):
    """
    Test that invalid input data (missing required fields) fails validation.
    """
    # Omitting 'name' and 'price' which are required.
    data = {
        "restaurant": restaurant.pk,
        "description": "Missing name and price",
        "category": "Food",
        "stock": 20,
        "available": True,
        "base64_image": "dummy"
    }
    serializer = ItemSerializer(data=data)
    assert not serializer.is_valid()
    # Expect errors for missing 'name' and 'price'.
    assert "name" in serializer.errors
    assert "price" in serializer.errors
