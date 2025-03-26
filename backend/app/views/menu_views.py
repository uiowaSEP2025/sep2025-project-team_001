from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from app.models.restaurant_models import Restaurant, Item
class MenuListCreateView(View):
    template_name = "menu_list.html"

    def get(self, request, *args, **kwargs):
        # Logic to retrieve and display the menu items

        restaurant = Restaurant.objects.first()
        items = restaurant.items.all() if restaurant else []

        return render(request, self.template_name, {
            'restairant': restaurant,
            'items': items
            })
    def post(self, request, *args, **kwargs):

        restaurant = Restaurant.objects.first()
        if not restaurant:
            return redirect('menu_list')
        
        
        name = request.POST.get('name')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category = request.POST.get('category')
        stock = request.POST.get('stock')
        available = bool(request.POST.get(available, True))

        Item.objects.create(
            restaurant=restaurant,
            name=name,
            description=description,
            price=price,
            category=category,
            stock=stock,
            available=available
        )

        return redirect('menu_list')
    
class MenuDetailView(View):
    template_name = 'menu_detail.html'

    def get(self, request, pk, *args, **kwargs):
        # Logic to retrieve and display the details of a specific menu item
        restaurant = Restaurant.objects.first()
        item = get_object_or_404(Item, pk=pk, restaurant=restaurant)

    

        

        

    