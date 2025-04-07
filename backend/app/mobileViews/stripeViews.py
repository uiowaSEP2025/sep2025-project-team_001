import stripe
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes

import json

stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(["POST"])
def create_payment_intent(request):
    try:
        data = json.loads(request.body)
        amount = data.get('amount')

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            automatic_payment_methods={"enabled": True},
        )

        return JsonResponse({'clientSecret': intent.client_secret})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@api_view(["POST"])
def create_setup_intent(request):
    try:
        data = json.loads(request.body)
        customer_id = data.get("customer_id")

        setup_intent = stripe.SetupIntent.create(
            customer=customer_id,
            payment_method_types=["card"],
        )

        return JsonResponse({'clientSecret': setup_intent.client_secret})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

def create_stripe_customer(email):
    customer = stripe.Customer.create(email=email)
    return customer.id
