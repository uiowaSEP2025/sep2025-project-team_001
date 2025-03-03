from django.http import JsonResponse
from .models import Customer

def get_customers(request):
    """Returns a list of all customers"""
    if request.method == "GET":
        customers = Customer.objects.select_related("user").all()
        data = {"customers": [customer.to_dict() for customer in customers]}
        return JsonResponse(data, status=200)

    return JsonResponse({"error": "Invalid request"}, status=400)

def get_customer_detail(request, pk):
    """Returns details of a specific customer"""
    if request.method == "GET":
        try:
            customer = Customer.objects.select_related("user").get(user__id=pk)
            return JsonResponse(customer.to_dict(), status=200)
        except Customer.DoesNotExist:
            return JsonResponse({"error": "Customer not found"}, status=404)

    return JsonResponse({"error": "Invalid request"}, status=400)