from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Restaurant
from ..models.restaurant_models import Item
from ..serializers.item_serializer import ItemSerializer
from ..serializers.restaurant_serializers import RestaurantSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_restaurants(request):
    restaurants = Restaurant.objects.all()
    serializer = RestaurantSerializer(restaurants, many=True)
    return Response(serializer.data)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_menu_items(request, restaurant_id):
    items = Item.objects.filter(restaurant__id=restaurant_id, available=True)
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)

