import pytest

from app.models.restaurant_models import Item
from app.models.restaurant_models import OrderItems


@pytest.mark.django_db
def test_order_items_str(customer, restaurant):
    """
    Ensure OrderItems.__str__ returns the correct description.
    """
    # Create an item for the order
    item_instance = Item.objects.create(
        restaurant=restaurant,
        name="Burger",
        description="Delicious burger",
        price="9.99",
        category="Food",
        stock=10,
        available=True,
        base64_image="samplebase64image"
    )
    quantity = 3
    cost = 29.97
    order_item = OrderItems.objects.create(
        customer=customer,
        restaurant=restaurant,
        item=item_instance,
        quantity=quantity,
        cost=cost
    )
    expected_str = f"{quantity} of {item_instance.name} from {restaurant.name}"
    assert str(order_item) == expected_str
