import json
from django.http import JsonResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def orders_webhook(request):

    try:
        data = json.loads(request.body)
    except json.JSONDecodeError:
        return HttpResponseBadRequest("Invalid JSON payload.")

    event_type = data.get("event_type")

    if event_type == "payment_success":
        handle_payment_success(data)
    elif event_type == "payment_failure":
        handle_payment_failure(data)
    else:
        return HttpResponseBadRequest("Unhandled event type.")

    return JsonResponse({"status": "success"})