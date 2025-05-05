from decimal import Decimal

import pytest
from app.models.order_models import Order, OrderItem
from app.models.restaurant_models import Ingredient, Item
from app.serializers.order_serializer import OrderItemSerializer


@pytest.mark.django_db
def test_order_item_serializer_representation_with_ingredients(customer, restaurant):
    """
    Representation should include:
      - item_name
      - quantity
      - unwanted_ingredients (IDs)
      - unwanted_ingredient_names (strings)
      - category (from Item)
    """
    order = Order.objects.create(customer=customer, restaurant=restaurant)
    item = Item.objects.create(
        restaurant=restaurant,
        name="Burger",
        description="Tasty burger",
        price=Decimal("9.99"),
        category="Food",
        stock=50,
        available=True,
        item_image_url="http://example.com/dummy.png",
    )

    pickle = Ingredient.objects.create(item=item, name="Pickles")
    onions = Ingredient.objects.create(item=item, name="Onions")

    order_item = OrderItem.objects.create(order=order, item=item, quantity=1)
    order_item.unwanted_ingredients.set([pickle, onions])

    serializer = OrderItemSerializer(order_item)
    data = serializer.data

    # Core fields
    assert data["item_name"] == "Burger"
    assert data["quantity"] == 1

    # IDs of unwanted ingredients
    assert sorted(data["unwanted_ingredients"]) == sorted([pickle.id, onions.id])
    # Names of unwanted ingredients
    assert sorted(data["unwanted_ingredient_names"]) == sorted([pickle.name, onions.name])
    # Category is correctly sourced
    assert data["category"] == "Food"


@pytest.mark.django_db
def test_order_item_serializer_deserialization_with_ingredients(customer, restaurant):
    """
    Deserialization should:
      - validate item_id, quantity, and unwanted_ingredients
      - map item_id → item, and unwanted_ingredients → Ingredient instances
    """
    Order.objects.create(customer=customer, restaurant=restaurant)
    item = Item.objects.create(
        restaurant=restaurant,
        name="Burger",
        description="Tasty burger",
        price=Decimal("9.99"),
        category="Food",
        stock=50,
        available=True,
        item_image_url="http://example.com/dummy.png",
    )

    ketchup = Ingredient.objects.create(item=item, name="Ketchup")
    mayo = Ingredient.objects.create(item=item, name="Mayo")

    payload = {
        "item_id": item.pk,
        "quantity": 2,
        "unwanted_ingredients": [ketchup.pk, mayo.pk],
    }

    serializer = OrderItemSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors

    validated = serializer.validated_data
    assert validated["item"] == item
    assert validated["quantity"] == 2
    assert sorted([i.id for i in validated["unwanted_ingredients"]]) == sorted([ketchup.id, mayo.id])


@pytest.mark.django_db
def test_missing_item_id_is_invalid():
    """
    Omitting 'item_id' should produce a validation error.
    """
    serializer = OrderItemSerializer(data={"quantity": 1})
    assert not serializer.is_valid()
    assert "item_id" in serializer.errors


@pytest.mark.django_db
def test_zero_quantity_is_valid(customer, restaurant):
    """
    A quantity of zero should be valid (PositiveIntegerField allows zero).
    """
    Order.objects.create(customer=customer, restaurant=restaurant)
    item = Item.objects.create(
        restaurant=restaurant,
        name="Test",
        description="",
        price=Decimal("1.00"),
        category="Food",
        stock=10,
        available=True,
        item_image_url="http://example.com/img.png",
    )

    serializer = OrderItemSerializer(data={"item_id": item.pk, "quantity": 0})
    assert serializer.is_valid(), serializer.errors
    validated = serializer.validated_data
    assert validated["quantity"] == 0
    assert validated["item"] == item


@pytest.mark.django_db
def test_invalid_unwanted_ingredient_id(customer, restaurant):
    """
    An unknown ingredient ID in unwanted_ingredients should error.
    """
    Order.objects.create(customer=customer, restaurant=restaurant)
    item = Item.objects.create(
        restaurant=restaurant,
        name="Test",
        description="",
        price=Decimal("1.00"),
        category="Food",
        stock=10,
        available=True,
        item_image_url="http://example.com/img.png",
    )

    serializer = OrderItemSerializer(data={
        "item_id": item.pk,
        "quantity": 1,
        "unwanted_ingredients": [9999],
    })
    assert not serializer.is_valid()
    assert "unwanted_ingredients" in serializer.errors


@pytest.mark.django_db
def test_extra_unexpected_fields_are_ignored(customer, restaurant):
    """
    Passing an unexpected field should be ignored, not cause errors.
    """
    Order.objects.create(customer=customer, restaurant=restaurant)
    item = Item.objects.create(
        restaurant=restaurant,
        name="Test",
        description="",
        price=Decimal("1.00"),
        category="Food",
        stock=10,
        available=True,
        item_image_url="http://example.com/img.png",
    )

    payload = {
        "item_id": item.pk,
        "quantity": 1,
        "foo": "bar"
    }
    serializer = OrderItemSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors
    assert "foo" not in serializer.validated_data
