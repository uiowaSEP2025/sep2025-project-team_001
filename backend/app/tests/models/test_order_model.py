from decimal import Decimal

import pytest

from app.models.order_models import Order
from app.models.order_models import OrderItem
from app.models.restaurant_models import Item


@pytest.mark.django_db
def test_order_str(customer, restaurant):
    """
    Ensure Order.__str__ returns the expected string.
    """
    order = Order.objects.create(
        customer=customer,
        restaurant=restaurant,
        status="pending",
        total_price=Decimal("0.00")
    )
    expected_str = f"Order #{order.id} by {customer.user.username} at {restaurant.name}"
    assert str(order) == expected_str


@pytest.mark.django_db
def test_order_get_total(customer, restaurant):
    """
    Ensure Order.get_total() returns the correct total price.
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
        name="Burger",
        description="Delicious burger",
        price=Decimal("9.99"),
        category="Food",
        stock=10,
        available=True,
        base64_image="dummy"
    )
    # Create an OrderItem for the order.
    order_item = OrderItem.objects.create(
        order=order,
        item=item_instance,
        quantity=3
    )
    expected_total = item_instance.price * order_item.quantity
    assert order.get_total() == expected_total
