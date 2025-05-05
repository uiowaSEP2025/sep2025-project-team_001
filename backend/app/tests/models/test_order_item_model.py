# app/tests/models/test_order_item_model.py
import pytest
from app.models.order_models import OrderItem
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_order_item_str(order_item):
    expected = f"{order_item.quantity}x {order_item.item.name} (Order #{order_item.order.id})"
    assert str(order_item) == expected


@pytest.mark.django_db
def test_order_item_default_quantity(order, burger_item):
    oi = OrderItem.objects.create(order=order, item=burger_item)
    assert oi.quantity == 1


@pytest.mark.django_db
def test_order_item_unwanted_ingredients(order_item, ingredients):
    # attach ingredients
    order_item.unwanted_ingredients.set(ingredients)
    stored = list(order_item.unwanted_ingredients.all())
    assert set(stored) == set(ingredients)


@pytest.mark.django_db
def test_negative_quantity_validation(order, burger_item):
    # Negative quantity should not pass model validation
    oi = OrderItem(order=order, item=burger_item, quantity=-1)
    with pytest.raises(ValidationError):
        oi.full_clean()


@pytest.mark.django_db
def test_duplicate_unwanted_ingredients_are_deduped(order_item, ingredients):
    # adding the same ingredient twice
    ing = ingredients[0]
    order_item.unwanted_ingredients.add(ing, ing)
    stored = list(order_item.unwanted_ingredients.all())
    assert stored.count(ing) == 1
