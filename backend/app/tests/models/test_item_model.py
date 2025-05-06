from decimal import Decimal

import pytest
from app.models.restaurant_models import Item
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_item_str_no_image(restaurant):
    """
    __str__ should use 'No image' when item_image_url is None.
    """
    item = Item.objects.create(
        restaurant=restaurant,
        name="Taco",
        price=Decimal("5.00"),
    )
    assert str(item) == "Taco (Image: No image)"


@pytest.mark.django_db
def test_item_str_with_image(restaurant):
    """
    __str__ should include the image URL when provided.
    """
    item = Item.objects.create(
        restaurant=restaurant,
        name="Taco",
        price=Decimal("5.00"),
        item_image_url="http://example.com/img.png"
    )
    assert str(item) == "Taco (Image: http://example.com/img.png)"


@pytest.mark.django_db
def test_default_field_values(restaurant):
    """
    Verify all defaults on a newly created Item.
    """
    item = Item.objects.create(
        restaurant=restaurant,
        name="Nachos",
        price=Decimal("3.50")
    )
    assert item.description == ""
    assert item.category == ""
    assert item.stock == 0
    assert item.available is True
    assert item.item_image_url is None
    assert item.times_ordered == 0


@pytest.mark.django_db
def test_item_in_restaurant_reverse_relation(restaurant):
    """
    restaurant.items should include this Item.
    """
    item = Item.objects.create(
        restaurant=restaurant,
        name="Quesadilla",
        price=Decimal("4.25")
    )
    assert item in restaurant.items.all()


@pytest.mark.django_db
def test_delete_restaurant_cascades_to_item(restaurant):
    """
    Deleting the parent Restaurant should delete its Items.
    """
    item = Item.objects.create(
        restaurant=restaurant,
        name="Burrito",
        price=Decimal("6.00")
    )
    restaurant.delete()
    assert not Item.objects.filter(pk=item.pk).exists()


@pytest.mark.django_db
def test_name_is_required(restaurant):
    """
    Blank name should trigger a ValidationError.
    """
    item = Item(
        restaurant=restaurant,
        name="",
        price=Decimal("1.00")
    )
    with pytest.raises(ValidationError):
        item.full_clean()


@pytest.mark.django_db
def test_invalid_image_url_validation(restaurant):
    """
    Non-URL in item_image_url should trigger a ValidationError.
    """
    item = Item(
        restaurant=restaurant,
        name="Taco",
        price=Decimal("2.00"),
        item_image_url="not-a-valid-url"
    )
    with pytest.raises(ValidationError):
        item.full_clean()


@pytest.mark.django_db
def test_unicode_name_and_description(restaurant):
    """
    Unicode in name/description should round-trip correctly.
    """
    name = "Téjano 🌮"
    desc = "Spicy & süß"
    item = Item.objects.create(
        restaurant=restaurant,
        name=name,
        description=desc,
        price=Decimal("5.50")
    )
    assert item.name == name
    assert item.description == desc


@pytest.mark.django_db
def test_name_max_length_validation(restaurant):
    """
    Exceeding 255 chars in name should trigger a ValidationError.
    """
    long_name = "x" * 256
    item = Item(
        restaurant=restaurant,
        name=long_name,
        price=Decimal("1.00")
    )
    with pytest.raises(ValidationError):
        item.full_clean()
