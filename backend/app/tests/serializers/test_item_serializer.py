from decimal import Decimal

import pytest

from app.models.restaurant_models import Item
from app.serializers.item_serializer import ItemSerializer


@pytest.mark.django_db
def test_item_serializer_representation(restaurant):
    # Create an Item instance associated with the given restaurant.
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
