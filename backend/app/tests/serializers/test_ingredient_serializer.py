import pytest
from app.models.restaurant_models import Ingredient
from app.serializers.ingredient_serializer import IngredientSerializer


@pytest.mark.django_db
def test_ingredient_serializer_output(burger_item):
    """
    IngredientSerializer should correctly serialize an Ingredient instance.
    """
    ingredient = Ingredient.objects.create(item=burger_item, name="Tomato")
    serialized = IngredientSerializer(ingredient)
    data = serialized.data

    assert set(data.keys()) == {"id", "name"}
    assert data["name"] == "Tomato"
    assert data["id"] == ingredient.id


@pytest.mark.django_db
def test_ingredient_serializer_input(burger_item):
    """
    IngredientSerializer should deserialize input data and create a valid Ingredient instance.
    """
    payload = {"name": "Lettuce"}
    serializer = IngredientSerializer(data=payload)

    assert serializer.is_valid()
    instance = serializer.save(item=burger_item)

    assert instance.name == "Lettuce"
    assert instance.item == burger_item
