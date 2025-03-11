import json
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework_simplejwt.tokens import RefreshToken
from .models import CustomUser

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

        if CustomUser.objects.filter(username=data["username"]).exists():
            return JsonResponse({"message": "Username already taken"}, status=400)

        if CustomUser.objects.filter(email=data["email"]).exists():
            return JsonResponse({"message": "Email already registered"}, status=400)

        user = CustomUser.objects.create_user(
            username=data["username"],
            email=data["email"],
            password=data["password"],
            first_name=data["name"],
            phone=data["phone"],
            business_name=data["business_name"],
            business_address=data["business_address"],
        )

        user.save()
        tokens = get_tokens_for_user(user)  # Generate JWT tokens

        return JsonResponse(
            {"message": "User registered successfully", "tokens": tokens}, status=201
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
            tokens = get_tokens_for_user(user)  # Generate JWT tokens
            return JsonResponse({"message": "Login successful", "tokens": tokens}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({"error": "Invalid request"}, status=400)
