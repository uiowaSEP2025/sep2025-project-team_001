from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from app.models import Restaurant
from app.models.restaurant_models import Item
from app.serializers.item_serializer import ItemSerializer
from app.serializers.restaurant_serializers import RestaurantSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_restaurants(request):
    restaurants = Restaurant.objects.all()
    serializer = RestaurantSerializer(restaurants, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_menu_items(request, restaurant):
    items = Item.objects.filter(restaurant__name=restaurant, available=True)
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)
