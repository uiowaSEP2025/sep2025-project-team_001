from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from app.models import PromotionNotification, Customer
from app.serializers.promotion_serializer import PromotionNotificationSerializer
from app.mobileViews.utils import send_notification_to_device

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_promotions(request):
    restaurant = request.user.restaurant
    promotions = PromotionNotification.objects.filter(restaurant=restaurant).order_by("-created_at")
    serializer = PromotionNotificationSerializer(promotions, many=True)
    return Response(serializer.data)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_promotion(request):
    data = request.data.copy()
    data['restaurant'] = request.user.restaurant.id
    serializer = PromotionNotificationSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_promotion(request, promotion_id):
    try:
        promotion = PromotionNotification.objects.get(id=promotion_id, restaurant=request.user.restaurant)
    except PromotionNotification.DoesNotExist:
        return Response({"error": "Promotion not found"}, status=status.HTTP_404_NOT_FOUND)

    serializer = PromotionNotificationSerializer(promotion, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_promotion(request, promotion_id):
    try:
        promotion = PromotionNotification.objects.get(id=promotion_id, restaurant=request.user.restaurant)
        promotion.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    except PromotionNotification.DoesNotExist:
        return Response({"error": "Promotion not found"}, status=status.HTTP_404_NOT_FOUND)

@api_view(["POST"])
@permission_classes([IsAuthenticated])
def send_promotion(request, promotion_id):
    try:
        promotion = PromotionNotification.objects.get(id=promotion_id, restaurant=request.user.restaurant)
    except PromotionNotification.DoesNotExist:
        return Response({"error": "Promotion not found"}, status=status.HTTP_404_NOT_FOUND)

    customers = Customer.objects.exclude(fcm_token__isnull=True).exclude(fcm_token="")

    for customer in customers:
        send_notification_to_device(
            device_token=customer.fcm_token,
            title=promotion.title,
            body=promotion.body,
            data={"type": "PROMOTION"}
        )

    promotion.sent = True
    promotion.save()

    return Response({"message": "Promotion sent!"})