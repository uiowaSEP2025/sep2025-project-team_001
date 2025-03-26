from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from app.models.restaurant_models import Restaurant, Item
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse

class MenuPageView(View):
    template_name = "menu_list.html"

    def get(self, request, *args, **kwargs):
        # Logic to retrieve and display the menu items

        restaurant = Restaurant.objects.first()
        items = restaurant.items.all() if restaurant else []

        return render(request, self.template_name, {
            'restaurant': restaurant,
            'items': items
            })
    def post(self, request, *args, **kwargs):
        action = request.POST.get('action', '')
        item_id = request.POST.get('item_id', None)
        restaurant = Restaurant.objects.first()
        if not restaurant:
            return redirect('menu_page')
        
        if action == 'create':
            name = request.POST.get('name')
            description = request.POST.get('description', '')
            price = float(request.POST.get('price', 0.0))
            category = request.POST.get('category', '')
            stock = int(request.POST.get('stock', 0))
            available = request.POST.get('available', 'false') == 'true'

            Item.objects.create(
                restaurant=restaurant,
                name=name,
                description=description,
                price=price,
                category=category,
                stock=stock,
                available=available
            )
        elif action == 'update' and item_id:
            item = get_object_or_404(Item, pk=item_id, restaurant=restaurant)
            item.name = request.POST.get('name', item.name)
            item.description = request.POST.get('description', item.description)
            item.price = float(request.POST.get('price', item.price))
            item.category = request.POST.get('category', item.category)
            item.stock = int(request.POST.get('stock', item.stock))
            item.available = request.POST.get('available', 'false') == 'true'
            item.save()
        elif action == 'delete' and item_id:
            item = get_object_or_404(Item, pk=item_id, restaurant=restaurant)
            item.delete()

        return redirect('menu_page')
    
def menu_items_api(request):
    if request.method == 'GET':
        restaurant = Restaurant.objects.first()
        if not restaurant:
            return JsonResponse({'error': 'Restaurant not found'}, status=404)
        items = list(restaurant.items.values())
        return JsonResponse({'items': items}, status=200)

        

        

    