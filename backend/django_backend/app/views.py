import json

from django.contrib.auth import authenticate, login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .models import CustomUser


@csrf_exempt
def register_user(request):
    if request.method == "POST":
        data = json.loads(request.body)

        if CustomUser.objects.filter(username=data["username"]).exists():
            return JsonResponse({"error": "Username already taken"}, status=400)

        if CustomUser.objects.filter(email=data["email"]).exists():
            return JsonResponse({"error": "Email already registered"}, status=400)

        # Create a new user with the extended fields
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

        return JsonResponse({"message": "User registered successfully"}, status=201)

    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def login_user(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login successful"}, status=200)
        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({"error": "Invalid request"}, status=400)
