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
    if not hasattr(request.user, "restaurant"):
        return Response(
            {"error": "Only restaurant accounts can view workers."},
            status=status.HTTP_403_FORBIDDEN,
        )

    restaurant = request.user.restaurant
    workers = Worker.objects.filter(restaurant=restaurant).values("id", "name", "pin", "role")
    return Response(list(workers), status=status.HTTP_200_OK)


@api_view(["PUT"])
@permission_classes([IsAuthenticated])
def update_worker(request, worker_id):
    try:
        worker = Worker.objects.get(id=worker_id)
    except Worker.DoesNotExist:
        return Response({"error": "Worker not found"}, status=404)

    data = request.data
    restaurant = worker.restaurant  # Get associated restaurant

    new_pin = data.get("pin", worker.pin)
    if new_pin != worker.pin:
        if Worker.objects.filter(pin=new_pin, restaurant=restaurant).exclude(id=worker.id).exists():
            return Response({"error": "PIN already in use for this restaurant"}, status=400)

    new_role = data.get("role", worker.role)
    if new_role not in ["manager", "bartender"]:
        return Response({"error": "Invalid role"}, status=400)

    worker.name = data.get("name", worker.name)
    worker.pin = new_pin
    worker.role = new_role
    worker.save()

    return Response({
        "message": "Worker updated successfully",
        "worker": {
            "id": worker.id,
            "name": worker.name,
            "role": worker.role,
            "pin": worker.pin
        }
    }, status=200)
