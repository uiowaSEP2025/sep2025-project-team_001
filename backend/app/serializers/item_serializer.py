from app.models import Item
from app.serializers.ingredient_serializer import IngredientSerializer
from rest_framework import serializers


class ItemSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True, read_only=True)
    item_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Item
        fields = "__all__"

    def get_item_image_url(self, obj):
        request = self.context.get("request")
        if obj.item_image_url and request:
            return request.build_absolute_uri(obj.item_image_url)
        return obj.item_image_url
