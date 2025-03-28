from decimal import Decimal

import pytest

from app.models.order_models import Order, OrderItem
from app.models.restaurant_models import Item


@pytest.mark.django_db
def test_order_item_str(customer, restaurant):
    """
    Ensure OrderItem.__str__ returns the correct description.
    """
    order = Order.objects.create(
        customer=customer,
        restaurant=restaurant,
        status="pending",
        total_price=Decimal("0.00")
    )
    item_instance = Item.objects.create(
        restaurant=restaurant,
        name="Pasta",
        description="Yummy pasta",
        price=Decimal("8.50"),
        category="Food",
        stock=10,
        available=True,
        base64_image="dummy"
    )
    order_item = OrderItem.objects.create(
        order=order,
        item=item_instance,
        quantity=2
    )
    expected_str = f"2x {item_instance.name} (Order #{order.id})"
    assert str(order_item) == expected_str


@pytest.mark.django_db
def test_order_item_multiple_entries(customer, restaurant):
    """
    Ensure that creating multiple OrderItem entries on one Order are correctly linked.
    """
    order = Order.objects.create(
        customer=customer,
        restaurant=restaurant,
        status="pending",
        total_price=Decimal("0.00")
    )
    item_instance = Item.objects.create(
        restaurant=restaurant,
        name="Sandwich",
        description="Tasty sandwich",
        price=Decimal("5.00"),
        category="Food",
        stock=15,
        available=True,
        base64_image="dummy"
    )
    # Create two order items for the same order.
    order_item1 = OrderItem.objects.create(order=order, item=item_instance, quantity=1)
    order_item2 = OrderItem.objects.create(order=order, item=item_instance, quantity=2)

    # Verify that both items are linked to the order.
    order_items = order.order_items.all()
    assert len(order_items) == 2
    # Verify string representations are correct.
    expected_str1 = f"{order_item1.quantity}x {item_instance.name} (Order #{order.id})"
    expected_str2 = f"{order_item2.quantity}x {item_instance.name} (Order #{order.id})"
    assert str(order_item1) == expected_str1
    assert str(order_item2) == expected_str2
