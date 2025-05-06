from decimal import Decimal

import pytest
from app.models.restaurant_models import Ingredient, Item
from app.serializers.item_serializer import ItemSerializer
from rest_framework.test import APIRequestFactory


@pytest.mark.django_db
def test_item_serializer_representation_with_ingredients(restaurant):
    """
    ItemSerializer should return correct serialized data including nested ingredients
    and use `item_image_url` instead of the old `base64_image`.
    """
    item = Item.objects.create(
        restaurant=restaurant,
        name="Loaded Burger",
        description="With toppings",
        price=Decimal("9.99"),
        category="Food",
        stock=100,
        available=True,
        item_image_url="http://example.com/image.png",
    )
    # Attach ingredients
    Ingredient.objects.create(item=item, name="Cheese")
    Ingredient.objects.create(item=item, name="Bacon")

    serializer = ItemSerializer(item)
    data = serializer.data

    assert data["id"] == item.id
    assert data["restaurant"] == restaurant.id
    assert data["name"] == "Loaded Burger"
    assert data["description"] == "With toppings"
    # price comes back as Decimal
    assert data["price"] == Decimal("9.99")
    assert data["category"] == "Food"
    assert data["stock"] == 100
    assert data["available"] is True
    assert data["item_image_url"] == "http://example.com/image.png"

    # Nested ingredients are dicts with id & name
    assert isinstance(data["ingredients"], list) and len(data["ingredients"]) == 2
    names = {ing["name"] for ing in data["ingredients"]}
    assert names == {"Cheese", "Bacon"}


@pytest.mark.django_db
def test_item_serializer_image_url_with_request(restaurant):
    """
    When a request is provided in context, `item_image_url` is built to an absolute URI.
    """
    factory = APIRequestFactory()
    req = factory.get("/dummy-path/")
    item = Item.objects.create(
        restaurant=restaurant,
        name="Picnic",
        price=Decimal("1.00"),
        item_image_url="/media/test.png"
    )
    serializer = ItemSerializer(item, context={"request": req})
    data = serializer.data

    assert data["item_image_url"].endswith("/media/test.png")


@pytest.mark.django_db
def test_item_serializer_deserialization_valid(restaurant):
    """
    Valid input data should deserialize and create a new Item.
    """
    payload = {
        "restaurant": restaurant.pk,
        "name": "Test Sandwich",
        "description": "A tasty sandwich",
        "price": "5.99",
        "category": "Food",
        "stock": 50,
        "available": True,
        # item_image_url is read-only; ignore on input
    }
    serializer = ItemSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors
    item = serializer.save()

    assert item.name == "Test Sandwich"
    assert item.description == "A tasty sandwich"
    assert item.price == Decimal("5.99")
    assert item.category == "Food"
    assert item.stock == 50
    assert item.available is True
    assert item.item_image_url is None
    assert item.restaurant == restaurant


@pytest.mark.django_db
def test_item_serializer_deserialization_missing_fields(restaurant):
    """
    Missing required fields (restaurant, name, price) should trigger errors.
    """
    payload = {
        "description": "Missing required",
        "stock": 20,
        "available": True,
    }
    serializer = ItemSerializer(data=payload)
    assert not serializer.is_valid()
    errs = serializer.errors
    assert "restaurant" in errs
    assert "name" in errs
    assert "price" in errs


@pytest.mark.django_db
def test_item_serializer_invalid_field_types(restaurant):
    """
    Non-numeric price or stock should fail.
    """
    payload = {
        "restaurant": restaurant.pk,
        "name": "Bad Data",
        "price": "free",
        "stock": "lots",
        "available": True,
    }
    serializer = ItemSerializer(data=payload)
    assert not serializer.is_valid()
    errs = serializer.errors
    assert "price" in errs
    assert "stock" in errs


@pytest.mark.django_db
def test_unicode_fields_roundtrip(restaurant):
    """
    Unicode in name & description should round-trip correctly.
    """
    name = "Téjano 🌮"
    desc = "Yummy & süß"
    item = Item.objects.create(
        restaurant=restaurant,
        name=name,
        description=desc,
        price=Decimal("5.50")
    )
    data = ItemSerializer(item).data
    assert data["name"] == name
    assert data["description"] == desc
