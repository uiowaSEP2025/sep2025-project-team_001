import json
import re
import unicodedata

import requests
from django.conf import settings
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken

from ..models.customer_models import CustomUser
from ..models.restaurant_models import Restaurant
from ..models.worker_models import Worker
from ..serializers.restaurant_serializer import RestaurantSerializer
from ..serializers.worker_serializer import WorkerSerializer


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)

        required_fields = [
            "name",
            "username",
            "password",
            "email",
            "phone",
            "business_name",
            "business_address",
            "restaurantImage",
            "pin",
        ]
        for field in required_fields:
            if not data.get(field):
                return JsonResponse(
                    {"message": f"{field.replace('_', ' ').capitalize()} is required."},
                    status=400,
                )

        if CustomUser.objects.filter(username=data["username"]).exists():
            return JsonResponse({"message": "Username already taken"}, status=400)

        if CustomUser.objects.filter(email=data["email"]).exists():
            return JsonResponse({"message": "Email already registered"}, status=400)

        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", data["email"]):
            return JsonResponse({"message": "Invalid email format."}, status=400)

        if not re.match(r"^\d{10}$", data["phone"]):
            return JsonResponse(
                {"message": "Phone number must be exactly 10 digits."}, status=400
            )

        if len(data["password"]) < 6:
            return JsonResponse(
                {"message": "Password must be at least 6 characters long."}, status=400
            )

        custom_user = CustomUser.objects.create_user(
            username=data["username"],
            email=data["email"],
            password=data["password"],
        )

        restaurant = Restaurant.objects.create(
            user=custom_user,
            name=data["business_name"],
            address=data["business_address"],
            phone=data["phone"],
            restaurant_image=data.get("restaurantImage")
        )

        # Create Worker (Manager role)
        worker = Worker.objects.create(
            restaurant=restaurant,
            name=data["name"],
            pin=data["pin"],
            role="manager"
        )

        restaurant_data = RestaurantSerializer(restaurant).data
        worker_data = WorkerSerializer(worker).data

        tokens = get_tokens_for_user(custom_user)  # Generate JWT tokens

        return JsonResponse(
            {
                "message": "User registered successfully",
                "tokens": tokens,
                "restaurant": restaurant_data,
                "worker": worker_data,
                "restaurant_id": restaurant.id,
            },
            status=201,
        )

    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def login_restaurant(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            try:
                restaurant = user.restaurant
                tokens = get_tokens_for_user(user)
                return JsonResponse({
                    "message": "Restaurant login successful",
                    "tokens": tokens,
                    "bar_name": restaurant.name,
                    "restaurant_id": restaurant.id,
                }, status=200)
            except Restaurant.DoesNotExist:
                return JsonResponse({"error": "User not linked to a restaurant."}, status=403)

        return JsonResponse({"error": "Invalid username or password."}, status=401)

    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        pin = data.get("pin")
        restaurant_id = data.get("restaurant_id")

        if not pin or not restaurant_id:
            return JsonResponse({"error": "PIN and restaurant_id are required."}, status=400)

        try:
            worker = Worker.objects.get(pin=pin, restaurant_id=restaurant_id)
            restaurant = worker.restaurant
            tokens = get_tokens_for_user(restaurant.user)

            return JsonResponse({
                "message": "Worker login successful",
                "tokens": tokens,
                "bar_name": restaurant.name,
                "restaurant_id": restaurant.id,
                "worker_id": worker.id,
                "role": worker.role,
            }, status=200)
        except Worker.DoesNotExist:
            return JsonResponse({"error": "Invalid PIN for this restaurant."}, status=401)

    return JsonResponse({"error": "Invalid request"}, status=400)


# Helper Function
def _norm(txt: str) -> str:
    txt = unicodedata.normalize("NFKD", txt).encode("ascii", "ignore").decode()
    return re.sub(r"[^\w\s]", "", txt).lower().strip()


@csrf_exempt
def validate_business(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            name, address = data["name"], data["address"]
        except (KeyError, TypeError, json.JSONDecodeError):
            return JsonResponse({"error": "name and address required"}, status=400)

        if not settings.GOOGLE_PLACES_API_KEY:
            return JsonResponse({"error": "Server mis‑config: key missing"}, status=500)

        params = {
            "input": f"{name}, {address}",
            "inputtype": "textquery",
            "fields": "place_id,name,formatted_address,business_status,types",
            "key": settings.GOOGLE_PLACES_API_KEY,
        }
        r = requests.get(
            "https://maps.googleapis.com/maps/api/place/findplacefromtext/json",
            params=params,
            timeout=6,
        ).json()

        if r.get("status") != "OK" or not r["candidates"]:
            return JsonResponse({"valid": False, "reason": "Place not found"}, status=400)

        cand = r["candidates"][0]
        if cand.get("business_status") == "CLOSED_PERMANENTLY":
            return JsonResponse({"valid": False, "reason": "Closed business"}, status=400)

        if _norm(address) not in _norm(cand["formatted_address"]):
            return JsonResponse({"valid": False, "reason": "Address mismatch"}, status=400)

        if not any(t in cand["types"] for t in ("bar", "restaurant")):
            return JsonResponse({"valid": False, "reason": "Not restaurant/bar"}, status=400)

        return JsonResponse({"valid": True, "place_id": cand["place_id"]}, status=200)
    return JsonResponse({"error": "Invalid request"}, status=400)
