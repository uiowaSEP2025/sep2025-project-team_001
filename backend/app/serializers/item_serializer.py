from app.models import Item
from app.serializers.ingredient_serializer import IngredientSerializer
from rest_framework import serializers


class ItemSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)

    class Meta:
        model = Item
        fields = "__all__"
