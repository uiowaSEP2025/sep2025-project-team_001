from decimal import Decimal

import pytest

from app.models.order_models import Order, OrderItem
from app.models.restaurant_models import Item
from app.serializers.order_serializer import OrderItemSerializer


@pytest.mark.django_db
def test_order_item_serializer(customer, restaurant):
    # Create an Item instance.
    item_instance = Item.objects.create(
        restaurant=restaurant,
        name="Burger",
        description="Tasty burger",
        price=Decimal("9.99"),
        category="Food",
        stock=50,
        available=True,
        base64_image="dummyimage"
    )
    # Create an Order instance.
    order = Order.objects.create(
        customer=customer,
        restaurant=restaurant,
        status="pending",
        total_price=Decimal("0.00")
    )
    order_item = OrderItem.objects.create(
        order=order,
        item=item_instance,
        quantity=2
    )
    serializer = OrderItemSerializer(order_item)
    data = serializer.data
    # Check that the serializer outputs the expected fields.
    assert "item" in data
    assert data["quantity"] == 2
