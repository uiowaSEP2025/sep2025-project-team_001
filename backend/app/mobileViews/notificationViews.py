from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
import json
from app.models.customer_models import Customer

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def save_fcm_token(request):
    data = json.loads(request.body)
    customer_id = data.get('customer_id')
    fcm_token = data.get('fcm_token')

    customer = Customer.objects.get(id=customer_id)
    customer.fcm_token = fcm_token
    customer.save()
    return JsonResponse({"message": "Token saved successfully"})
