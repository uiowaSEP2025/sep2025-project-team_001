from decimal import Decimal

import pytest
from app.models.order_models import Order, OrderItem
from django.utils import timezone


@pytest.mark.django_db
def test_order_str(order):
    """
    The string representation of an Order should include ID, customer, and restaurant.
    """
    expected = f"Order #{order.id} by {order.customer.user.username} at {order.restaurant.name}"
    assert str(order) == expected


@pytest.mark.django_db
def test_order_defaults(customer, restaurant):
    """
    When an Order is created, its default fields should be correctly set.
    """
    order = Order.objects.create(customer=customer, restaurant=restaurant)
    assert order.status == "pending"
    assert order.total_price == Decimal("0.00")
    assert order.start_time is not None
    assert order.estimated_pickup_time is None
    assert (timezone.now() - order.start_time).total_seconds() < 60


@pytest.mark.django_db
def test_order_set_estimated_pickup_time(order):
    """
    Tests that we can set and retrieve the estimated_pickup_time on an Order.
    """
    now = timezone.now()
    # Set an ETA 30 minutes from now.
    eta = now + timezone.timedelta(minutes=30)
    order.estimated_pickup_time = eta
    order.save()
    order.refresh_from_db()
    assert order.estimated_pickup_time == eta


@pytest.mark.django_db
def test_order_get_total(order, burger_item):
    """
    Order.get_total should return the correct sum of all order item prices.
    """
    item_price = burger_item.price
    OrderItem.objects.create(order=order, item=burger_item, quantity=2)
    OrderItem.objects.create(order=order, item=burger_item, quantity=3)

    expected_total = item_price * 5
    assert order.get_total() == expected_total
