# app/tests/models/test_order_model.py
from decimal import Decimal

import pytest
from app.models.order_models import OrderItem


@pytest.mark.django_db
def test_order_defaults(order):
    # Defaults on new order
    assert order.start_time is None
    assert order.total_price == Decimal("0.00")
    assert order.order_items.count() == 0
    assert order.status == "pending"
    assert order.food_status == "pending"
    assert order.beverage_status == "pending"
    assert order.reviewed is False
    assert order.worker is None


@pytest.mark.django_db
def test_order_items_relationship(order_item, order):
    # order_items reverse relationship
    assert list(order.order_items.all()) == [order_item]


@pytest.mark.django_db
def test_cascade_delete_order_deletes_items(order_item):
    # Deleting order cascades to OrderItem
    order = order_item.order
    order.delete()
    assert not OrderItem.objects.filter(pk=order_item.pk).exists()


@pytest.mark.django_db
def test_str_representation(order):
    # __str__ includes id, username, restaurant name
    s = str(order)
    assert f"Order #{order.id}" in s
    assert order.customer.user.username in s
    assert order.restaurant.name in s


@pytest.mark.django_db
def test_get_total(order, burger_item):
    # get_total sums price * quantity
    burger_item.price = Decimal("5.00")
    burger_item.save()
    OrderItem.objects.create(order=order, item=burger_item, quantity=2)
    assert order.get_total() == Decimal("10.00")
