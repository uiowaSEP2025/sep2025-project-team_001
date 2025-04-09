from decimal import Decimal

import pytest
from app.models.order_models import Order, OrderItem
from app.models.restaurant_models import Ingredient, Item


@pytest.mark.django_db
def test_order_item_str(customer, restaurant):
    order = Order.objects.create(customer=customer, restaurant=restaurant)
    item = Item.objects.create(
        restaurant=restaurant, name="Pasta", price=Decimal("8.50"),
        description="Pasta", category="Food", stock=10,
        available=True, base64_image="img"
    )
    order_item = OrderItem.objects.create(order=order, item=item, quantity=2)
    assert str(order_item) == f"2x Pasta (Order #{order.id})"


@pytest.mark.django_db
def test_order_item_multiple(customer, restaurant):
    order = Order.objects.create(customer=customer, restaurant=restaurant)
    item = Item.objects.create(
        restaurant=restaurant, name="Sandwich", price=Decimal("5.00"),
        description="Sandwich", category="Food", stock=10,
        available=True, base64_image="img"
    )
    oi1 = OrderItem.objects.create(order=order, item=item, quantity=1)
    oi2 = OrderItem.objects.create(order=order, item=item, quantity=2)

    items = order.order_items.all()
    assert len(items) == 2
    assert str(oi1) == f"1x Sandwich (Order #{order.id})"
    assert str(oi2) == f"2x Sandwich (Order #{order.id})"


@pytest.mark.django_db
def test_order_item_unwanted_ingredients(customer, restaurant):
    order = Order.objects.create(customer=customer, restaurant=restaurant)
    item = Item.objects.create(
        restaurant=restaurant, name="Loaded Burger", price=Decimal("10.00"),
        description="Everything on it", category="Food", stock=10,
        available=True, base64_image="img"
    )

    pickles = Ingredient.objects.create(item=item, name="Pickles")
    onions = Ingredient.objects.create(item=item, name="Onions")

    order_item = OrderItem.objects.create(order=order, item=item, quantity=1)
    order_item.unwanted_ingredients.set([pickles, onions])

    unwanted = order_item.unwanted_ingredients.all()
    assert unwanted.count() == 2
    assert pickles in unwanted
    assert onions in unwanted
