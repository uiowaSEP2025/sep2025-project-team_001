# backend/views/worker_views.py
import json
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from ..models.restaurant_models import Restaurant
from ..models.worker_models import Worker

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_worker(request):
    data = request.data  # DRF automatically parses JSON

    pin = data.get("pin")
    role = data.get("role")
    name = data.get("name")
    restaurant_id = data.get("restaurant_id")

    if not (pin and role and restaurant_id):
        return Response({"error": "Missing required fields"}, status=status.HTTP_400_BAD_REQUEST)

    if Worker.objects.filter(pin=pin, restaurant_id=restaurant_id).exists():
        return Response({"error": "PIN already in use for this restaurant"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        restaurant = Restaurant.objects.get(id=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response({"error": "Restaurant not found"}, status=status.HTTP_404_NOT_FOUND)

    worker = Worker.objects.create(
        restaurant=restaurant,
        name=name,
        pin=pin,
        role=role
    )

    return Response({
        "message": f"{role.title()} created successfully",
        "worker_id": worker.id,
        "name": worker.name
    }, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_workers(request):
    try:
        restaurant = request.user.restaurant
    except Restaurant.DoesNotExist:
        return Response({"error": "Restaurant not found for this user"}, status=status.HTTP_404_NOT_FOUND)

    workers = Worker.objects.filter(restaurant=restaurant).values("id", "name", "pin", "role")
    return Response(list(workers), status=status.HTTP_200_OK)