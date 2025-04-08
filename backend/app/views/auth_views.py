import json
import re

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken

from ..models.customer_models import CustomUser
from ..models.restaurant_models import Restaurant
from ..models.worker_models import Worker


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
            return JsonResponse(
                {"message": "Phone number must be exactly 10 digits."}, status=400
            )

        # Validate password length
        if len(data["password"]) < 6:
            return JsonResponse(
                {"message": "Password must be at least 6 characters long."}, status=400
            )

        # Create the user account first
        custom_user = CustomUser.objects.create_user(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            first_name=data["name"]
        )

        # Then create the restaurant profile tied to that user
        restaurant = Restaurant.objects.create(
            user=custom_user,
            name=data["business_name"],
            address=data["business_address"],
            phone=data["phone"],
            restaurant_image=data.get("restaurantImage")
        )


        # Create Worker (Manager role)
        Worker.objects.create(
            restaurant=restaurant,
            pin=data["pin"],
            role="manager"
        )

        tokens = get_tokens_for_user(custom_user)  # Generate JWT tokens

        return JsonResponse(
            {
                "message": "User registered successfully",
                "tokens": tokens,
                "restaurant": restaurant.name,
                "restaurant_id": restaurant.id,
            },
            status=201,
        )

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            try:
                restaurant = user.restaurant  # works if OneToOneField exists
                tokens = get_tokens_for_user(user)

                return JsonResponse(
                    {
                        "message": "Login successful",
                        "tokens": tokens,
                        "bar_name": restaurant.name,
                        "restaurant_id": restaurant.id,
                    },
                    status=200,
                )
            except Restaurant.DoesNotExist:
                return JsonResponse({"error": "This user is not linked to a restaurant."}, status=403)

        return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({"error": "Invalid request"}, status=400)
