from rest_framework import serializers
from ..models import Restaurant


class RestaurantSerializer(serializers.ModelSerializer):
    restaurant_image_url = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = "__all__"

    def get_restaurant_image_url(self, obj):
        request = self.context.get("request")
        if obj.restaurant_image_url and request:
            return request.build_absolute_uri(obj.restaurant_image_url)
        return obj.restaurant_image_url
