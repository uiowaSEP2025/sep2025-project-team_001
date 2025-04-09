# backend/views/worker_views.py
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json

from ..models.worker_models import Worker
from ..models.restaurant_models import Restaurant
from ..models.customer_models import CustomUser


@csrf_exempt
def create_worker(request):
    if request.method == "POST":
        data = json.loads(request.body)

        pin = data.get("pin")
        role = data.get("role")
        restaurant_id = data.get("restaurant_id")

        if not (pin and role and restaurant_id):
            return JsonResponse({"error": "Missing required fields"}, status=400)

        if Worker.objects.filter(pin=pin, restaurant_id=restaurant_id).exists():
            return JsonResponse({"error": "PIN already in use for this restaurant"}, status=400)

        try:
            restaurant = Restaurant.objects.get(id=restaurant_id)
        except Restaurant.DoesNotExist:
            return JsonResponse({"error": "Restaurant not found"}, status=404)

        worker = Worker.objects.create(
            pin=pin,
            role=role,
            restaurant=restaurant
        )

        return JsonResponse({
            "message": f"{role.title()} created successfully",
            "worker_id": worker.id
        }, status=201)

    return JsonResponse({"error": "Invalid request"}, status=400)