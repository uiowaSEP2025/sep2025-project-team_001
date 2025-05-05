# app/tests/serializers/test_order_serializer.py

from decimal import Decimal

import pytest
from app.models.restaurant_models import Ingredient, Item
from app.serializers.order_serializer import OrderSerializer


@pytest.mark.django_db
def test_order_serializer_create(customer, restaurant):
    """
    OrderSerializer should validate and save an order with item(s) and unwanted ingredients,
    and leave all ETA/status fields null or default by default.
    """
    # Create an Item using the current field name
    item = Item.objects.create(
        restaurant=restaurant,
        name="Burger",
        description="Test burger",
        price=Decimal("9.99"),
        category="Food",
        stock=20,
        available=True,
        item_image_url="http://example.com/test.png"
    )
    # Create two unwanted ingredients
    ing1 = Ingredient.objects.create(item=item, name="Pickles")
    ing2 = Ingredient.objects.create(item=item, name="Onions")

    # Prepare the payload
    payload = {
        "customer_id": customer.id,
        "restaurant_id": restaurant.id,
        "order_items": [
            {
                "item_id": item.id,
                "quantity": 1,
                "unwanted_ingredients": [ing1.id, ing2.id],
            }
        ],
    }

    # Validate & save
    serializer = OrderSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors
    order = serializer.save()

    # Refresh & serialize the created Order
    data = OrderSerializer(order).data

    # Basic fields
    assert data["restaurant_id_read"] == restaurant.id
    assert data["customer_name"] == customer.user.first_name or customer.user.username
    assert data["restaurant_name"] == restaurant.name

    # Check order_items payload
    order_items = data["order_items"]
    assert isinstance(order_items, list) and len(order_items) == 1
    item_data = order_items[0]
    assert item_data["item_name"] == "Burger"
    assert item_data["quantity"] == 1
    assert sorted(item_data["unwanted_ingredients"]) == sorted([ing1.id, ing2.id])
    assert sorted(item_data["unwanted_ingredient_names"]) == sorted([ing1.name, ing2.name])
    assert item_data["category"] == "Food"

    # ETA & status fields should be null/default
    assert data["estimated_food_ready_time"] is None
    assert data["estimated_beverage_ready_time"] is None
    assert data["food_eta_minutes"] is None
    assert data["beverage_eta_minutes"] is None
    assert data["status"] == "pending"
    assert data["food_status"] == "pending"
    assert data["beverage_status"] == "pending"
    assert data["reviewed"] is False
    assert data.get("worker_name") is None

    # Total price should be a string
    assert data["total_price"] == Decimal("0.00")


@pytest.mark.django_db
def test_order_serializer_missing_required_fields():
    """
    Omitting required keys results in validation errors.
    """
    serializer = OrderSerializer(data={})
    assert not serializer.is_valid()
    errs = serializer.errors
    assert "customer_id" in errs
    assert "restaurant_id" in errs
    assert "order_items" in errs


@pytest.mark.django_db
def test_order_serializer_invalid_quantity_and_item(customer, restaurant):
    """
    Negative or zero quantity, or invalid item_id, should be caught.
    """
    # Zero quantity
    payload = {
        "customer_id": customer.id,
        "restaurant_id": restaurant.id,
        "order_items": [{"item_id": 9999, "quantity": 0}],
    }
    serializer = OrderSerializer(data=payload)
    assert not serializer.is_valid()
    errs = serializer.errors["order_items"][0]
    assert "quantity" in errs or "item_id" in errs


@pytest.mark.django_db
def test_order_serializer_extra_unexpected_fields(customer, restaurant):
    """
    Passing unexpected fields should produce errors.
    """
    payload = {
        "customer_id": customer.id,
        "restaurant_id": restaurant.id,
        "order_items": [],
        "foo": "bar"
    }
    serializer = OrderSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors
    assert "foo" not in serializer.validated_data
