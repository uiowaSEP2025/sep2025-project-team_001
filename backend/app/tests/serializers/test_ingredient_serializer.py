import pytest
from app.models.restaurant_models import Ingredient
from app.serializers.ingredient_serializer import IngredientSerializer


@pytest.mark.django_db
def test_ingredient_serializer_output(burger_item):
    """
    IngredientSerializer should correctly serialize an Ingredient instance.
    """
    ingredient = Ingredient.objects.create(item=burger_item, name="Tomato")
    serializer = IngredientSerializer(ingredient)
    data = serializer.data

    # Only id & name fields
    assert set(data.keys()) == {"id", "name"}
    assert data["id"] == ingredient.id
    assert data["name"] == "Tomato"


@pytest.mark.django_db
def test_ingredient_serializer_input_valid(burger_item):
    """
    Valid input should deserialize and create an Ingredient.
    """
    payload = {"name": "Lettuce"}
    serializer = IngredientSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors

    instance = serializer.save(item=burger_item)
    assert isinstance(instance, Ingredient)
    assert instance.name == "Lettuce"
    assert instance.item == burger_item


@pytest.mark.django_db
def test_missing_name_is_invalid(burger_item):
    """
    Omitting 'name' yields a validation error.
    """
    serializer = IngredientSerializer(data={})
    assert not serializer.is_valid()
    assert "name" in serializer.errors


@pytest.mark.django_db
def test_blank_name_is_invalid(burger_item):
    """
    Blank name should not pass validation.
    """
    serializer = IngredientSerializer(data={"name": ""})
    assert not serializer.is_valid()
    assert "name" in serializer.errors


@pytest.mark.django_db
def test_name_max_length_validation(burger_item):
    """
    Name longer than 100 chars should fail.
    """
    long_name = "x" * 101
    serializer = IngredientSerializer(data={"name": long_name})
    assert not serializer.is_valid()
    assert "name" in serializer.errors


@pytest.mark.django_db
def test_name_accepts_non_string_and_coerces_to_str(burger_item):
    """
    Non-string values for name are coerced to strings.
    """
    serializer = IngredientSerializer(data={"name": 123})
    assert serializer.is_valid(), serializer.errors
    inst = serializer.save(item=burger_item)
    assert inst.name == "123"


@pytest.mark.django_db
def test_unicode_name_roundtrip(burger_item):
    """
    Unicode characters in name are preserved in output.
    """
    text = "酸辣 🌶️"
    ingredient = Ingredient.objects.create(item=burger_item, name=text)
    data = IngredientSerializer(ingredient).data
    assert data["name"] == text
