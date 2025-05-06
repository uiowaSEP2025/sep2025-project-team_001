import pytest
from app.models.restaurant_models import Ingredient
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_ingredient_str(burger_item):
    """
    __str__ returns the ingredient’s own name.
    """
    ing = Ingredient.objects.create(item=burger_item, name="Tomato")
    assert str(ing) == "Tomato"


@pytest.mark.django_db
def test_ingredient_belongs_to_item(burger_item):
    """
    The Ingredient appears in item.ingredients reverse relation.
    """
    ing = Ingredient.objects.create(item=burger_item, name="Lime")
    assert ing in burger_item.ingredients.all()


@pytest.mark.django_db
def test_delete_item_deletes_ingredient(burger_item):
    """
    Deleting the parent Item cascades to remove its Ingredient.
    """
    ing = Ingredient.objects.create(item=burger_item, name="Pepper")
    burger_item.delete()
    assert not Ingredient.objects.filter(pk=ing.pk).exists()


@pytest.mark.django_db
def test_name_required(burger_item):
    """
    An empty name should not pass model validation.
    """
    ing = Ingredient(item=burger_item, name="")
    with pytest.raises(ValidationError):
        ing.full_clean()


@pytest.mark.django_db
def test_name_max_length(burger_item):
    """
    Exceeding max_length=100 triggers validation error.
    """
    long_name = "x" * 101
    ing = Ingredient(item=burger_item, name=long_name)
    with pytest.raises(ValidationError):
        ing.full_clean()


@pytest.mark.django_db
def test_unicode_name(burger_item):
    """
    Non‐ASCII characters in name are preserved.
    """
    name = "酸辣 🌶️"
    ing = Ingredient.objects.create(item=burger_item, name=name)
    assert ing.name == name
