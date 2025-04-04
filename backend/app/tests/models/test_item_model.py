from decimal import Decimal

import pytest
from app.models.restaurant_models import Item


@pytest.mark.django_db
def test_item_str_with_image(restaurant):
    """
    Ensure Item.__str__ shows an image preview when a base64 image is provided.
    """
    image_str = "abcdefghijklmnopqrstuvwxyz0123456789"
    item_instance = Item.objects.create(
        restaurant=restaurant,
        name="Pizza",
        description="Tasty pizza",
        price=Decimal("12.50"),
        category="Food",
        stock=5,
        available=True,
        base64_image=image_str,
    )
    expected_preview = image_str[:30] + "..."
    expected_str = f"Pizza (Image: {expected_preview})"
    assert str(item_instance) == expected_str


@pytest.mark.django_db
def test_item_str_without_image(restaurant):
    """
    Ensure Item.__str__ indicates 'No image' when no base64 image is provided.
    """
    item_instance = Item.objects.create(
        restaurant=restaurant,
        name="Salad",
        description="Fresh salad",
        price=Decimal("7.99"),
        category="Food",
        stock=8,
        available=True,
        base64_image=None,
    )
    expected_str = "Salad (Image: No image)"
    assert str(item_instance) == expected_str


@pytest.mark.django_db
def test_item_relationship(restaurant):
    """
    Ensure that an Item is correctly linked to its Restaurant.
    """
    item_instance = Item.objects.create(
        restaurant=restaurant,
        name="Sandwich",
        description="Tasty sandwich",
        price=Decimal("6.50"),
        category="Food",
        stock=20,
        available=True,
        base64_image="dummyimage",
    )
    assert item_instance.restaurant == restaurant
