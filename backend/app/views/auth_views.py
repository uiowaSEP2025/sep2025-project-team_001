import json
import re

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken

from ..models.customer_models import CustomUser, Manager
from ..models.restaurant_models import Restaurant


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

        # Check if all fields are present and non-empty
        required_fields = [
            "name", "username", "password", "email",
            "phone", "business_name", "business_address"
        ]
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({"message": f"{field.replace('_', ' ').capitalize()} is required."}, status=400)

        # Check if username is already taken
        if CustomUser.objects.filter(username=data["username"]).exists():
            return JsonResponse({"message": "Username already taken"}, status=400)

        # Check if email is already registered
        if CustomUser.objects.filter(email=data["email"]).exists():
            return JsonResponse({"message": "Email already registered"}, status=400)

        # Validate email format
        if not re.match(r"^[^@]+@[^@]+\.[^@]+$", data["email"]):
            return JsonResponse({"message": "Invalid email format."}, status=400)

        # Validate phone number (must be 10 digits)
        if not re.match(r"^\d{10}$", data["phone"]):
            return JsonResponse({"message": "Phone number must be exactly 10 digits."}, status=400)

        # Validate password length
        if len(data["password"]) < 6:
            return JsonResponse({"message": "Password must be at least 6 characters long."}, status=400)

        # Create custom user for username, email, password, and name
        user = CustomUser.objects.create_user(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            first_name=data["name"],
        )

        # Create Manager profile
        manager = Manager.objects.create(user=user)

        # Create Restaurant and add manager to the restaurant
        restaurant = Restaurant.objects.create(
            name=data["business_name"],
            address=data["business_address"],
            phone=data["phone"],
            restaurant_image=data.get("restaurantImage")
        )
        restaurant.managers.add(manager)

        tokens = get_tokens_for_user(user)  # Generate JWT tokens

        return JsonResponse({
            "message": "User registered successfully",
            "tokens": tokens,
            "manager": manager.user.username,
            "restaurant": restaurant.name,
            "restaurant_image": restaurant.restaurant_image[:30] + "..." if restaurant.restaurant_image else None,
            "restaurant_managers": [m.user.username for m in restaurant.managers.all()]
        }, status=201)

    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            tokens = get_tokens_for_user(user)  # Generate JWT tokens
            return JsonResponse({"message": "Login successful", "tokens": tokens}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({"error": "Invalid request"}, status=400)
