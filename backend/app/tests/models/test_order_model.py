from decimal import Decimal

import pytest
from app.models.order_models import Order, OrderItem
from django.utils import timezone


@pytest.mark.django_db
def test_order_str(order):
    expected = f"Order #{order.id} by {order.customer.user.username} at {order.restaurant.name}"
    assert str(order) == expected


@pytest.mark.django_db
def test_order_defaults(customer, restaurant):
    order = Order.objects.create(customer=customer, restaurant=restaurant)
    assert order.status == "pending"
    assert order.total_price == Decimal("0.00")
    assert order.start_time is not None
    assert (timezone.now() - order.start_time).total_seconds() < 60


@pytest.mark.django_db
def test_order_get_total(order, burger_item):
    item_price = burger_item.price
    OrderItem.objects.create(order=order, item=burger_item, quantity=2)
    OrderItem.objects.create(order=order, item=burger_item, quantity=3)

    expected_total = item_price * 5
    assert order.get_total() == expected_total
