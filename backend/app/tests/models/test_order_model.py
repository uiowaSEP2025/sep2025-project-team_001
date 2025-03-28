from decimal import Decimal

import pytest
from django.utils import timezone

from app.models.order_models import Order, OrderItem
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
def test_order_default_fields(customer, restaurant):
    """
    Ensure that default values for status and total_price are correctly set,
    and that start_time is autopopulated.
    """
    order = Order.objects.create(
        customer=customer,
        restaurant=restaurant,
    )
    # Check that default values are set correctly
    assert order.status == "pending"
    assert order.total_price == Decimal("0.00")
    assert order.start_time is not None
    # Check that start_time is reasonably recent (within a minute)
    assert (timezone.now() - order.start_time).total_seconds() < 60


@pytest.mark.django_db
def test_order_get_total(customer, restaurant):
    """
    Ensure Order.get_total() returns the correct total price when multiple order items exist.
    """
    order = Order.objects.create(
        customer=customer,
        restaurant=restaurant,
        status="pending",
        total_price=Decimal("0.00")
    )
    # Create two items for testing
    item1 = Item.objects.create(
        restaurant=restaurant,
        name="Burger",
        description="Delicious burger",
        price=Decimal("9.99"),
        category="Food",
        stock=10,
        available=True,
        base64_image="dummy"
    )
    item2 = Item.objects.create(
        restaurant=restaurant,
        name="Fries",
        description="Crispy fries",
        price=Decimal("3.50"),
        category="Food",
        stock=20,
        available=True,
        base64_image="dummy"
    )
    # Create OrderItems
    OrderItem.objects.create(order=order, item=item1, quantity=2)
    OrderItem.objects.create(order=order, item=item2, quantity=3)

    expected_total = (item1.price * 2) + (item2.price * 3)
    assert order.get_total() == expected_total
