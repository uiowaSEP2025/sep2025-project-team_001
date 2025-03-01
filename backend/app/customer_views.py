from django.http import JsonResponse
from .models import Customer

def get_customers(request):
    if request.method == "GET":
        customers = Customer.objects.all()
        data = {"customers": list(customers.values())}
        return JsonResponse(data, status=200)
    return JsonResponse({"error": "Invalid request"}, status=400)
