from decimal import Decimal

import pytest
from app.models.order_models import Order, OrderItem
from app.models.restaurant_models import Ingredient, Item
from app.serializers.order_serializer import OrderItemSerializer


@pytest.mark.django_db
def test_order_item_serializer_representation_with_ingredients(customer, restaurant):
    """
    OrderItemSerializer should correctly serialize unwanted ingredients in the output.
    """
    order = Order.objects.create(customer=customer, restaurant=restaurant)
    item = Item.objects.create(
        restaurant=restaurant,
        name="Burger",
        description="Tasty burger",
        price=Decimal("9.99"),
        category="Food",
        stock=50,
        available=True,
        base64_image="dummyimage",
    )

    pickle = Ingredient.objects.create(item=item, name="Pickles")
    onions = Ingredient.objects.create(item=item, name="Onions")

    order_item = OrderItem.objects.create(order=order, item=item, quantity=1)
    order_item.unwanted_ingredients.set([pickle, onions])

    serializer = OrderItemSerializer(order_item)
    data = serializer.data

    assert data["item_name"] == "Burger"
    assert data["quantity"] == 1
    assert sorted(data["unwanted_ingredients"]) == sorted([pickle.id, onions.id])


@pytest.mark.django_db
def test_order_item_serializer_deserialization_with_ingredients(customer, restaurant):
    """
    OrderItemSerializer should correctly deserialize and validate input with unwanted ingredients.
    """
    Order.objects.create(customer=customer, restaurant=restaurant)
    item = Item.objects.create(
        restaurant=restaurant,
        name="Burger",
        description="Tasty burger",
        price=Decimal("9.99"),
        category="Food",
        stock=50,
        available=True,
        base64_image="dummyimage",
    )

    ketchup = Ingredient.objects.create(item=item, name="Ketchup")
    mayo = Ingredient.objects.create(item=item, name="Mayo")

    payload = {
        "item_id": item.pk,
        "quantity": 2,
        "unwanted_ingredients": [ketchup.pk, mayo.pk],
    }

    serializer = OrderItemSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors

    validated = serializer.validated_data
    assert validated["item"] == item
    assert validated["quantity"] == 2
    assert sorted([i.id for i in validated["unwanted_ingredients"]]) == sorted([ketchup.id, mayo.id])
