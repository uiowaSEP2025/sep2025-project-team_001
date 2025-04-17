# app/tests/utils/test_order_model.py

from decimal import Decimal

import pytest
from django.utils import timezone
from datetime import timedelta

from app.models.order_models import Order, OrderItem
from app.models.restaurant_models import Item


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

    # New ETA fields should default to None
    assert order.estimated_food_ready_time is None
    assert order.estimated_beverage_ready_time is None

    # start_time was auto_now_add, so it should be very recent
    assert (timezone.now() - order.start_time).total_seconds() < 60


@pytest.mark.django_db
def test_set_estimated_etas(order):
    """
    Tests that we can set and retrieve both ETA fields on an Order.
    """
    now = timezone.now().replace(second=0, microsecond=0)
    food_eta = now + timedelta(minutes=30)
    bev_eta  = now + timedelta(minutes=15)

    # Assign and save
    order.estimated_food_ready_time = food_eta
    order.estimated_beverage_ready_time = bev_eta
    order.save()
    order.refresh_from_db()

    assert order.estimated_food_ready_time == food_eta
    assert order.estimated_beverage_ready_time == bev_eta


@pytest.mark.django_db
def test_order_get_total(order, burger_item):
    """
    Order.get_total should return the correct sum of all order item prices.
    """
    item_price = burger_item.price
    OrderItem.objects.create(order=order, item=burger_item, quantity=2)
    OrderItem.objects.create(order=order, item=burger_item, quantity=3)

    expected_total = item_price * Decimal(5)
    assert order.get_total() == expected_total
