import pytest
from app.models.restaurant_models import Ingredient


@pytest.mark.django_db
def test_ingredient_str(burger_item):
    ingredient = Ingredient.objects.create(item=burger_item, name="Lettuce")
    assert str(ingredient) == "Lettuce"
    assert ingredient.item == burger_item
