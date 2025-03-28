from decimal import Decimal

import pytest

from app.models.restaurant_models import Item
from app.serializers.order_serializer import OrderSerializer


@pytest.mark.django_db
def test_order_serializer_create(customer, restaurant):
    # Create an Item to be ordered.
    item_instance = Item.objects.create(
        restaurant=restaurant,
        name="Pizza",
        description="Cheesy pizza",
        price=Decimal("12.50"),
        category="Food",
        stock=20,
        available=True,
        base64_image="dummyimage"
    )
    # Prepare input data for the OrderSerializer.
    data = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [
            {"item_id": item_instance.pk, "quantity": 3}
        ]
    }
    serializer = OrderSerializer(data=data)
    assert serializer.is_valid(), serializer.errors
    order = serializer.save()
    assert order.customer == customer
    assert order.restaurant == restaurant
    assert order.order_items.count() == 1
    order_item = order.order_items.first()
    assert order_item.item == item_instance
    assert order_item.quantity == 3
