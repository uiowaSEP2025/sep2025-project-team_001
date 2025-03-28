import json
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from app.models.restaurant_models import Restaurant, Item

@csrf_exempt
def menu_items_api(request):
    if request.method == 'GET':
        restaurant = Restaurant.objects.first()
        if not restaurant:
            return JsonResponse({'error': 'Restaurant not found'}, status=404)

        items = list(restaurant.items.values())
        return JsonResponse({'items': items}, status=200)

    return JsonResponse({'error': 'Method not allowed'}, status=405)


@csrf_exempt
def manage_menu_item(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        action = data.get('action')
        item_id = data.get('item_id')
        restaurant = Restaurant.objects.first()

        if not restaurant:
            return JsonResponse({'error': 'Restaurant not found'}, status=404)

        if action == 'create':
            required_fields = ['name', 'price', 'category', 'stock', 'image']
            for field in required_fields:
                if field not in data or not data[field]:
                    return JsonResponse({'error': f"{field} is required"}, status=400)

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
            return JsonResponse({
                'message': 'Item created successfully',
                'item_id': item.id,
                'item_str': str(item)
            }, status=201)

        elif action == 'update' and item_id:
            item = get_object_or_404(Item, pk=item_id, restaurant=restaurant)

            item.name = data.get('name', item.name)
            item.description = data.get('description', item.description)
            item.price = float(data.get('price', item.price))
            item.category = data.get('category', item.category)
            item.stock = int(data.get('stock', item.stock))
            item.available = data.get('available', item.available)
            item.base64_image = data['image']
            item.save()

            return JsonResponse({'message': 'Item updated successfully'}, status=200)

        elif action == 'delete' and item_id:
            item = get_object_or_404(Item, pk=item_id, restaurant=restaurant)
            item.delete()
            return JsonResponse({'message': 'Item deleted successfully'}, status=200)

        return JsonResponse({'error': 'Invalid action or missing item_id'}, status=400)

    return JsonResponse({'error': 'Method not allowed'}, status=405)