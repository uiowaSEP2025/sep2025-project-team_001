from decimal import Decimal

import pytest
from app.models.restaurant_models import Ingredient, Item


@pytest.mark.django_db
def test_item_str_with_image(restaurant):
    """
    The string representation should include the item name and truncated base64 image if present.
    """
    image = "abcdefghijklmnopqrstuvwxyz0123456789"
    item = Item.objects.create(
        restaurant=restaurant,
        name="Pizza",
        description="Tasty",
        price=Decimal("12.50"),
        category="Food",
        stock=5,
        available=True,
        base64_image=image
    )
    assert str(item) == f"Pizza (Image: {image[:30]}...)"


@pytest.mark.django_db
def test_item_str_without_image(restaurant):
    """
    If no base64 image is present, the string should indicate 'No image'.
    """
    item = Item.objects.create(
        restaurant=restaurant,
        name="Salad",
        description="Fresh",
        price=Decimal("7.99"),
        category="Food",
        stock=8,
        available=True,
        base64_image=None
    )
    assert str(item) == "Salad (Image: No image)"


@pytest.mark.django_db
def test_item_relationship(restaurant):
    """
    The item's restaurant field should correctly link to the given restaurant.
    """
    item = Item.objects.create(
        restaurant=restaurant,
        name="Sandwich",
        description="Tasty",
        price=Decimal("6.50"),
        category="Food",
        stock=20,
        available=True,
        base64_image="dummy"
    )
    assert item.restaurant == restaurant


@pytest.mark.django_db
def test_item_with_ingredients(restaurant):
    """
    Ingredients related to the item should be accessible via the reverse relationship.
    """
    item = Item.objects.create(
        restaurant=restaurant,
        name="Custom Pizza",
        description="With toppings",
        price=Decimal("15.00"),
        category="Food",
        stock=10,
        available=True,
        base64_image="image"
    )
    cheese = Ingredient.objects.create(item=item, name="Cheese")
    pepperoni = Ingredient.objects.create(item=item, name="Pepperoni")

    ingredients = item.ingredients.all()
    assert cheese in ingredients
    assert pepperoni in ingredients
