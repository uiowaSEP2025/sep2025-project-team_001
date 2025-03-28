import pytest

from app.models.restaurant_models import Item


@pytest.mark.django_db
def test_item_str_without_image(restaurant):
    """
    Ensure Item.__str__ indicates 'No image' when no base64 image is provided.
    """
    item_instance = Item.objects.create(
        restaurant=restaurant,
        name="Burger",
        description="Delicious burger",
        price="9.99",
        category="Food",
        stock=10,
        available=True,
        base64_image=None
    )
    expected_str = f"{item_instance.name} (Image: No image)"
    assert str(item_instance) == expected_str


@pytest.mark.django_db
def test_item_str_with_image(restaurant):
    """
    Ensure Item.__str__ shows an image preview when a base64 image is provided.
    """
    image_str = "abcdefghijklmnopqrstuvwxyz0123456789"
    item_instance = Item.objects.create(
        restaurant=restaurant,
        name="Burger",
        description="Delicious burger",
        price="9.99",
        category="Food",
        stock=10,
        available=True,
        base64_image=image_str
    )
    expected_preview = image_str[:30] + "..."
    expected_str = f"{item_instance.name} (Image: {expected_preview})"
    assert str(item_instance) == expected_str
