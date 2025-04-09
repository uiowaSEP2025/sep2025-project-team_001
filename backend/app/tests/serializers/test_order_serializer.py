from decimal import Decimal

import pytest
from app.models.order_models import Order, OrderItem
from app.models.restaurant_models import Ingredient, Item
from app.serializers.order_serializer import OrderSerializer


@pytest.mark.django_db
def test_order_serializer_create(customer, restaurant):
    item = Item.objects.create(
        restaurant=restaurant,
        name="Burger",
        description="Test burger",
        price=Decimal("9.99"),
        category="Food",
        stock=20,
        available=True,
        base64_image="img"
    )

    pickle = Ingredient.objects.create(item=item, name="Pickles")
    onions = Ingredient.objects.create(item=item, name="Onions")

    payload = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "status": "pending",
        "total_price": "19.98",
        "order_items": [
            {
                "item_id": item.pk,
                "quantity": 2,
                "unwanted_ingredients": [pickle.pk, onions.pk],
            }
        ],
    }

    serializer = OrderSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors
    order = serializer.save()

    assert order.customer == customer
    assert order.restaurant == restaurant
    assert order.status == "pending"
    assert order.total_price == Decimal("19.98")
    assert order.order_items.count() == 1

    order_item = order.order_items.first()
    assert order_item.item == item
    assert order_item.quantity == 2
    assert set(order_item.unwanted_ingredients.all()) == {pickle, onions}


@pytest.mark.django_db
def test_order_serializer_representation(order, burger_item, ingredients):
    # Create an order item
    order_item = OrderItem.objects.create(order=order, item=burger_item, quantity=1)
    order_item.unwanted_ingredients.set(ingredients)

    serializer = OrderSerializer(order)
    data = serializer.data

    assert data["id"] == order.id
    assert data["customer_name"] == order.customer.user.first_name
    assert data["restaurant_name"] == order.restaurant.name
    assert len(data["order_items"]) == 1
    item_data = data["order_items"][0]
    assert item_data["item_name"] == burger_item.name
    assert item_data["quantity"] == 1
    assert sorted(item_data["unwanted_ingredients"]) == sorted([i.id for i in ingredients])
