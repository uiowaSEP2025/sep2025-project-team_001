from django.http import JsonResponse


def login(request):
    return JsonResponse({"message": "Login endpoint", "status": "success"}, status=200)
