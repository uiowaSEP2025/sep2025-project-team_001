from decimal import Decimal

import pytest
from app.models.order_models import Order, OrderItem
from app.models.restaurant_models import Item
from app.serializers.order_serializer import OrderItemSerializer


@pytest.mark.django_db
def test_order_item_serializer_representation(customer, restaurant):
    """
    Test that OrderItemSerializer returns the expected output for an existing OrderItem.
    """
    # Create an Order and an Item.
    order = Order.objects.create(
        customer=customer,
        restaurant=restaurant,
        status="pending",
        total_price=Decimal("0.00"),
    )
    item_instance = Item.objects.create(
        restaurant=restaurant,
        name="Burger",
        description="Tasty burger",
        price=Decimal("9.99"),
        category="Food",
        stock=50,
        available=True,
        base64_image="dummyimage",
    )
    # Create an OrderItem.
    order_item = OrderItem.objects.create(order=order, item=item_instance, quantity=2)
    serializer = OrderItemSerializer(order_item)
    data = serializer.data
    assert "item_name" in data
    assert data["item_name"] == "Burger"
    assert data["quantity"] == 2


@pytest.mark.django_db
def test_order_item_serializer_deserialization(customer, restaurant):
    """
    Test direct validation of OrderItemSerializer input data.
    """
    # Create an Order and an Item.
    Order.objects.create(
        customer=customer,
        restaurant=restaurant,
        status="pending",
        total_price=Decimal("0.00"),
    )
    item_instance = Item.objects.create(
        restaurant=restaurant,
        name="Burger",
        description="Tasty burger",
        price=Decimal("9.99"),
        category="Food",
        stock=50,
        available=True,
        base64_image="dummyimage",
    )
    # Prepare input data for OrderItemSerializer.
    data = {"item_id": item_instance.pk, "quantity": 4}
    serializer = OrderItemSerializer(data=data)
    # Validate that the serializer accepts the input.
    assert serializer.is_valid(), serializer.errors
    validated_data = serializer.validated_data
    # The validated data should map 'item_id' to the actual item instance via the 'item' field.
    assert validated_data["item"] == item_instance
    assert validated_data["quantity"] == 4
