from decimal import Decimal

import pytest

from app.models.order_models import Order, OrderItem
from app.models.restaurant_models import Item


@pytest.mark.django_db
def test_order_item_str(customer, restaurant):
    """
    Ensure OrderItem.__str__ returns the correct description.
    """
    # Create an Order instance.
    order = Order.objects.create(
        customer=customer,
        restaurant=restaurant,
        status="pending",
        total_price=Decimal("0.00")
    )
    # Create an Item instance.
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
    # Create an OrderItem.
    order_item = OrderItem.objects.create(
        order=order,
        item=item_instance,
        quantity=2
    )
    expected_str = f"2x {item_instance.name} (Order #{order.id})"
    assert str(order_item) == expected_str
