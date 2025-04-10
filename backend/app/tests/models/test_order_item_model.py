from decimal import Decimal

import pytest
from app.models.order_models import Order, OrderItem
from app.models.restaurant_models import Ingredient, Item


@pytest.mark.django_db
def test_order_item_str(order, burger_item):
    """
    The string representation of an OrderItem should include item name and quantity.
    """
    order_item = OrderItem.objects.create(order=order, item=burger_item, quantity=2)
    assert str(order_item) == f"2x {burger_item.name} (Order #{order.id})"


@pytest.mark.django_db
def test_order_item_multiple(order, burger_item):
    """
    Creating multiple OrderItems for the same order should result in multiple linked entries.
    """
    oi1 = OrderItem.objects.create(order=order, item=burger_item, quantity=1)
    oi2 = OrderItem.objects.create(order=order, item=burger_item, quantity=2)

    items = order.order_items.all()
    assert len(items) == 2
    assert str(oi1) == f"1x {burger_item.name} (Order #{order.id})"
    assert str(oi2) == f"2x {burger_item.name} (Order #{order.id})"


@pytest.mark.django_db
def test_order_item_unwanted_ingredients(order, burger_item, ingredients):
    """
    Unwanted ingredients should be correctly assigned to the OrderItem.
    """
    order_item = OrderItem.objects.create(order=order, item=burger_item, quantity=1)
    order_item.unwanted_ingredients.set(ingredients)

    unwanted = order_item.unwanted_ingredients.all()
    assert set(unwanted) == set(ingredients)
