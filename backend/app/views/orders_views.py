from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models.order_models import Order
from ..serializers.order_serializer import OrderSerializer


@api_view(["POST"])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    if serializer.is_valid():
        order = serializer.save()

        order.total_price = order.get_total()
        order.save()

        return Response(
            {"message": "Order created successfully", "order_id": order.id},
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def retrieve_active_orders(request):
    try:
        manager = request.user.manager  # Get the logged-in user's Manager profile
        restaurant = manager.restaurants.first()
    except:
        return Response(
            {"error": "Manager or restaurant not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    orders = (
        Order.objects.filter(restaurant=restaurant)
        .prefetch_related("order_items__item", "customer__user")
        .order_by("-start_time")
    )

    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def mark_order_completed(request, order_id):
    try:
        order = Order.objects.get(pk=order_id)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    order.status = "completed"
    order.save()
    return Response(
        {"message": "Order marked as completed.", "order_id": order.id},
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_customer_orders(request):
    try:
        customer = request.user.customer

    except:
        return Response(
            {"error": "Manager or restaurant not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    orders = (
        Order.objects.filter(customer=customer)
        .prefetch_related("order_items__item", "customer__user")
        .order_by("-start_time")
    )

    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
