import json

from app.mobileViews.stripeViews import create_stripe_customer
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from ..models import Customer, CustomUser
from ..views.auth_views import get_tokens_for_user


@csrf_exempt
def register_customer(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)

            email = data.get("email")
            password = data.get("password")
            name = data.get("name")

            if CustomUser.objects.filter(username=email).exists():
                return JsonResponse({"message": "Email already in use"}, status=400)

            user = CustomUser.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=name
            )

            stripe_customer_id = create_stripe_customer(email)

            customer = Customer.objects.create(
                user=user,
                stripe_customer_id=stripe_customer_id
            )

            tokens = get_tokens_for_user(user)

            return JsonResponse(
                {
                    "message": "User registered successfully",
                    "tokens": tokens,
                    "customer_id": customer.id,
                    "stripe_customer_id": stripe_customer_id,
                    "name": customer.user.first_name
                },
                status=201
            )

        except Exception as e:
            return JsonResponse(
                {"message": "Registration failed", "error": str(e)},
                status=500
            )

    return JsonResponse({"error": "Invalid request"}, status=400)


@csrf_exempt
def login_customer(request):
    if request.method == "POST":
        data = json.loads(request.body)
        username = data.get("username")
        password = data.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            tokens = get_tokens_for_user(user)
            return JsonResponse({"message": "Login successful", "tokens": tokens, "customer_id": getattr(user.customer, 'id', None), "name": getattr(user.customer.user, 'first_name', None)}, status=200)

        else:
            return JsonResponse({"error": "Invalid credentials"}, status=401)

    return JsonResponse({"error": "Invalid request"}, status=400)
