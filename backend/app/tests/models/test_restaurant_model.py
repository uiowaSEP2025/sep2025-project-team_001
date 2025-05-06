# app/tests/models/test_restaurant_model.py
import pytest
from app.models.restaurant_models import Item, Restaurant
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_restaurant_str_and_user(restaurant, custom_user):
    """
    __str__ returns the restaurant’s name,
    and the user FK matches the fixture’s user.
    """
    assert str(restaurant) == restaurant.name
    assert restaurant.user == custom_user


@pytest.mark.django_db
def test_restaurant_unicode_fields(restaurant):
    """
    Non‐ASCII in name and address round‐trip correctly.
    """
    restaurant.name = "Café José 🚀"
    restaurant.address = "123 Calle 🌞"
    restaurant.save()
    reloaded = Restaurant.objects.get(pk=restaurant.pk)
    assert reloaded.name == "Café José 🚀"
    assert reloaded.address == "123 Calle 🌞"


@pytest.mark.django_db
def test_required_fields_validation(restaurant):
    """
    Blank name/address/phone should trigger ValidationError.
    """
    user = restaurant.user
    bad = Restaurant(user=user, name="", address="", phone="")
    with pytest.raises(ValidationError):
        bad.full_clean()


@pytest.mark.django_db
def test_items_reverse_relation_and_cascade_delete(restaurant, burger_item):
    """
    Items created under a restaurant appear in restaurant.items,
    and deleting the restaurant cascades to its items.
    """
    # The burger_item fixture was created with this restaurant
    assert burger_item in restaurant.items.all()

    # Deleting the restaurant should remove its items
    item_pk = burger_item.pk
    restaurant.delete()
    assert not Item.objects.filter(pk=item_pk).exists()


@pytest.mark.django_db
def test_cascade_delete_user_deletes_restaurant(restaurant, custom_user):
    """
    Deleting the CustomUser cascades to delete their restaurants.
    """
    user = custom_user
    rest_pk = restaurant.pk
    user.delete()
    assert not Restaurant.objects.filter(pk=rest_pk).exists()
