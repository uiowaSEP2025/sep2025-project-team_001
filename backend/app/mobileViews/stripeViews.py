import json

import stripe
from django.conf import settings
from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated

stripe.api_key = settings.STRIPE_SECRET_KEY

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_payment_intent(request):
    try:
        data = json.loads(request.body)
        amount = data.get('amount')
        save_card = data.get('save_card', False)

        customer = request.user.customer

        payment_intent_data = {
            "amount": amount,
            "currency": "usd",
            "customer": customer.stripe_customer_id,
            "automatic_payment_methods": {"enabled": True},
        }

        if save_card:
            payment_intent_data["setup_future_usage"] = "off_session"

        intent = stripe.PaymentIntent.create(**payment_intent_data)

        return JsonResponse({
            'client_secret': intent.client_secret,
            'customer_id': customer.stripe_customer_id,
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_saved_payment_methods(request):
    customer = request.user.customer

    try:
        payment_methods = stripe.PaymentMethod.list(
            customer=customer.stripe_customer_id,
            type="card"
        )

        methods_data = [{
            "id": pm.id,
            "brand": pm.card.brand,
            "last4": pm.card.last4,
            "exp_month": pm.card.exp_month,
            "exp_year": pm.card.exp_year,
        } for pm in payment_methods.data]

        return JsonResponse({"paymentMethods": methods_data})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def pay_with_saved_card(request):
    try:
        data = json.loads(request.body)
        amount = data.get('amount')
        payment_method_id = data.get('payment_method_id')

        customer = request.user.customer

        intent = stripe.PaymentIntent.create(
            amount=amount,
            currency='usd',
            customer=customer.stripe_customer_id,
            payment_method=payment_method_id,
            off_session=True,
            confirm=True,
        )

        return JsonResponse({'status': intent.status})
    except stripe.error.CardError as e:
        return JsonResponse({'error': str(e.user_message)}, status=402)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_payment_method(request, payment_method_id):
    try:
        stripe.PaymentMethod.detach(payment_method_id)

        return JsonResponse({"message": "Payment method detached successfully"})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


def create_stripe_customer(email):
    customer = stripe.Customer.create(email=email)
    return customer.id
