# app/tests/models/test_order_model.py
from datetime import datetime
from decimal import Decimal

import pytest
from app.models.order_models import OrderItem


@pytest.mark.django_db
def test_order_defaults(order):
    # start_time auto-set
    assert isinstance(order.start_time, datetime)
    # total_price default
    assert order.total_price == Decimal("0.00")
    # no items yet
    assert order.order_items.count() == 0


@pytest.mark.django_db
def test_order_items_relationship(order_item, order):
    # the fixture-created item appears in the reverse relation
    assert list(order.order_items.all()) == [order_item]


@pytest.mark.django_db
def test_cascade_delete_order_deletes_items(order_item):
    order = order_item.order
    order.delete()
    assert not OrderItem.objects.filter(pk=order_item.pk).exists()
