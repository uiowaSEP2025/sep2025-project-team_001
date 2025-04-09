import pytest
from app.models import Ingredient


@pytest.mark.django_db
def test_ingredient_str(restaurant, item):
    """
    The string representation of an Ingredient should return its name.
    """
    ingredient = Ingredient.objects.create(item=item, name="Tomato")
    assert str(ingredient) == "Tomato"
