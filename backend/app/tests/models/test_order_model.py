from decimal import Decimal

import pytest
from app.models.order_models import Order, OrderItem
from app.models.restaurant_models import Item
from django.utils import timezone


@pytest.mark.django_db
def test_order_str(customer, restaurant):
    order = Order.objects.create(customer=customer, restaurant=restaurant)
    expected = f"Order #{order.id} by {customer.user.username} at {restaurant.name}"
    assert str(order) == expected


@pytest.mark.django_db
def test_order_defaults(customer, restaurant):
    order = Order.objects.create(customer=customer, restaurant=restaurant)
    assert order.status == "pending"
    assert order.total_price == Decimal("0.00")
    assert order.start_time is not None
    assert (timezone.now() - order.start_time).total_seconds() < 60


@pytest.mark.django_db
def test_order_get_total(customer, restaurant):
    order = Order.objects.create(customer=customer, restaurant=restaurant)

    item1 = Item.objects.create(
        restaurant=restaurant, name="Burger", price=Decimal("9.99"),
        description="Burger", category="Food", stock=10,
        available=True, base64_image="img"
    )
    item2 = Item.objects.create(
        restaurant=restaurant, name="Fries", price=Decimal("3.50"),
        description="Fries", category="Food", stock=10,
        available=True, base64_image="img"
    )

    OrderItem.objects.create(order=order, item=item1, quantity=2)
    OrderItem.objects.create(order=order, item=item2, quantity=3)

    expected_total = (item1.price * 2) + (item2.price * 3)
    assert order.get_total() == expected_total
