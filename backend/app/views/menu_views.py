from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models.restaurant_models import Item, Restaurant


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def menu_items_api(request):
    if request.method == "GET":
        if not hasattr(request.user, "restaurant"):
            return Response({"error": "Only restaurant accounts can access this."}, status=403)

        restaurant = request.user.restaurant
        items = Item.objects.filter(restaurant=restaurant).values()
        return Response({"items": list(items)}, status=200)

    return Response({"error": "Method not allowed"}, status=405)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def manage_menu_item(request):
    if not hasattr(request.user, "restaurant"):
        return Response({"error": "Only restaurant accounts can manage menu items."}, status=403)

    restaurant = request.user.restaurant
    data = request.data
    action = data.get("action")
    item_id = data.get("item_id")

    if action == "create":
        required_fields = ["name", "price", "category", "stock", "image"]
        for field in required_fields:
            if field not in data or not data[field]:
                return Response(
                    {"error": f"{field} is required"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        item = Item.objects.create(
            restaurant=restaurant,
            name=data["name"],
            description=data.get("description", ""),
            price=float(data["price"]),
            category=data["category"],
            stock=int(data["stock"]),
            available=data.get("available", False),
            base64_image=data.get("image"),
        )
        return Response(
            {
                "message": "Item created successfully",
                "item_id": item.id,
                "item_str": str(item),
            },
            status=status.HTTP_201_CREATED,
        )

    elif action == "update" and item_id:
        item = get_object_or_404(Item, pk=item_id, restaurant=restaurant)

        item.name = data.get("name", item.name)
        item.description = data.get("description", item.description)
        item.price = float(data.get("price", item.price))
        item.category = data.get("category", item.category)
        item.stock = int(data.get("stock", item.stock))
        item.available = data.get("available", item.available)
        item.base64_image = data.get("image", item.base64_image)
        item.save()

        return Response(
            {"message": "Item updated successfully"}, status=status.HTTP_200_OK
        )

    elif action == "delete" and item_id:
        item = get_object_or_404(Item, pk=item_id, restaurant=restaurant)
        item.delete()
        return Response(
            {"message": "Item deleted successfully"}, status=status.HTTP_200_OK
        )

    return Response(
        {"error": "Invalid action or missing item_id"},
        status=status.HTTP_400_BAD_REQUEST,
    )
