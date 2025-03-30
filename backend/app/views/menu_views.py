import json
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from ..models.restaurant_models import Restaurant, Item
from rest_framework import status


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def menu_items_api(request):
    if request.method == 'GET':
        try:
            manager = request.user.manager  # Assumes OneToOne with user
            restaurant = manager.restaurants.first()
        except:
            return Response({'error': 'Manager or restaurant not found'}, status=404)

        items = Item.objects.filter(restaurant=restaurant).values()
        return Response({'items': list(items)}, status=200)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def manage_menu_item(request):
    data = request.data
    action = data.get('action')
    item_id = data.get('item_id')

    try:
        manager = request.user.manager
        restaurant = manager.restaurants.first()
    except:
        return Response({'error': 'Manager or restaurant not found'}, status=status.HTTP_404_NOT_FOUND)

    if not restaurant:
        return Response({'error': 'Restaurant not found'}, status=status.HTTP_404_NOT_FOUND)

    if action == 'create':
        required_fields = ['name', 'price', 'category', 'stock', 'image']
        for field in required_fields:
            if field not in data or not data[field]:
                return Response({'error': f"{field} is required"}, status=status.HTTP_400_BAD_REQUEST)

        item = Item.objects.create(
            restaurant=restaurant,
            name=data['name'],
            description=data.get('description', ''),
            price=float(data['price']),
            category=data['category'],
            stock=int(data['stock']),
            available=data.get('available', False),
            base64_image=data.get('image')
        )
        return Response({
            'message': 'Item created successfully',
            'item_id': item.id,
            'item_str': str(item)
        }, status=status.HTTP_201_CREATED)

    elif action == 'update' and item_id:
        item = get_object_or_404(Item, pk=item_id, restaurant=restaurant)

        item.name = data.get('name', item.name)
        item.description = data.get('description', item.description)
        item.price = float(data.get('price', item.price))
        item.category = data.get('category', item.category)
        item.stock = int(data.get('stock', item.stock))
        item.available = data.get('available', item.available)
        item.base64_image = data.get('image', item.base64_image)
        item.save()

        return Response({'message': 'Item updated successfully'}, status=status.HTTP_200_OK)

    elif action == 'delete' and item_id:
        item = get_object_or_404(Item, pk=item_id, restaurant=restaurant)
        item.delete()
        return Response({'message': 'Item deleted successfully'}, status=status.HTTP_200_OK)

    return Response({'error': 'Invalid action or missing item_id'}, status=status.HTTP_400_BAD_REQUEST)
