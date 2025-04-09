from decimal import Decimal

import pytest
from app.models.restaurant_models import Ingredient, Item
from app.serializers.item_serializer import ItemSerializer


@pytest.mark.django_db
def test_item_serializer_representation_with_ingredients(restaurant):
    """
    ItemSerializer should return correct serialized data including nested ingredients.
    """
    item = Item.objects.create(
        restaurant=restaurant,
        name="Loaded Burger",
        description="With toppings",
        price=Decimal("9.99"),
        category="Food",
        stock=100,
        available=True,
        base64_image="base64img"
    )
    Ingredient.objects.create(item=item, name="Cheese")
    Ingredient.objects.create(item=item, name="Bacon")

    serializer = ItemSerializer(item)
    data = serializer.data

    assert data["id"] == item.id
    assert data["name"] == item.name
    assert data["description"] == item.description
    assert data["price"] == item.price
    assert data["category"] == item.category
    assert data["stock"] == item.stock
    assert data["available"] is True
    assert data["base64_image"] == item.base64_image
    assert data["restaurant"] == restaurant.id

    # Check nested ingredients
    assert len(data["ingredients"]) == 2
    ingredient_names = [ingredient["name"] for ingredient in data["ingredients"]]
    assert "Cheese" in ingredient_names
    assert "Bacon" in ingredient_names


@pytest.mark.django_db
def test_item_serializer_deserialization_valid(restaurant):
    """
    Valid input data should deserialize correctly and produce a new Item instance.
    """
    data = {
        "restaurant": restaurant.pk,
        "name": "Test Sandwich",
        "description": "A tasty sandwich",
        "price": "5.99",
        "category": "Food",
        "stock": 50,
        "available": True,
        "base64_image": "somedummystring",
    }
    serializer = ItemSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    item = serializer.save()

    assert item.name == "Test Sandwich"
    assert item.description == "A tasty sandwich"
    assert item.price == Decimal("5.99")
    assert item.category == "Food"
    assert item.stock == 50
    assert item.available is True
    assert item.base64_image == "somedummystring"
    assert item.restaurant == restaurant


@pytest.mark.django_db
def test_item_serializer_deserialization_invalid(restaurant):
    """
    Missing required fields (name, price) should trigger serializer validation errors.
    """
    data = {
        "restaurant": restaurant.pk,
        "description": "Missing name and price",
        "category": "Food",
        "stock": 20,
        "available": True,
        "base64_image": "dummy",
    }
    serializer = ItemSerializer(data=data)
    assert not serializer.is_valid()
    assert "name" in serializer.errors
    assert "price" in serializer.errors
