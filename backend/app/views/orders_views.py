from app.models.restaurant_models import Restaurant
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models.order_models import Order
from ..serializers.order_serializer import OrderSerializer
from ..models.worker_models import Worker


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
    if not hasattr(request.user, "restaurant"):
        return Response(
            {"error": "Only restaurant accounts can view active orders."},
            status=status.HTTP_403_FORBIDDEN,
        )

    restaurant = request.user.restaurant
    orders = (
        Order.objects.filter(restaurant=restaurant)
        .prefetch_related("order_items__item", "customer__user")
        .order_by("-start_time")
    )

    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_order_status(request, order_id, new_status, restaurant_id):
    # if not hasattr(request.user, "restaurant"):
    #     return Response(
    #         {"error": "Only restaurant accounts can update orders."},
    #         status=status.HTTP_403_FORBIDDEN,
    #     )

    # Normalize status (e.g., 'Picked Up' → 'picked_up')
    normalized_status = new_status.lower().replace(" ", "_")

    # List of allowed statuses
    valid_statuses = ["pending", "in_progress", "completed", "picked_up", "cancelled"]
    if normalized_status not in valid_statuses:
        return Response(
            {"error": f"Invalid status '{new_status}'."},
            status=status.HTTP_400_BAD_REQUEST,
        )

    try:
        restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response(
            {"error": "Restaurant not found."},
            status=status.HTTP_404_NOT_FOUND,
    )

    try:
        order = Order.objects.get(pk=order_id, restaurant=restaurant)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    if normalized_status == "cancelled" and order.status != "pending":
        return Response(
            {"error": f"Invalid status '{new_status}'."},
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    if normalized_status == "in_progress" and order.status == "pending":
        worker_id = request.data.get("worker_id")
        if not worker_id:
            return Response({"error": "Missing worker ID."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            worker = Worker.objects.get(id=worker_id)
            order.worker = worker
        except Worker.DoesNotExist:
            return Response({"error": "Worker not found."}, status=status.HTTP_404_NOT_FOUND)

    order.status = normalized_status
    order.save()
    return Response(
        {
            "message": f"Order status updated to '{normalized_status}'.",
            "order_id": order.id,
            "status": normalized_status,
        },
        status=status.HTTP_200_OK,
    )


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_customer_orders(request):
    try:
        customer = request.user.customer  # request.user is CustomUser here
    except:
        return Response(
            {"error": "Customer not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    orders = (
        Order.objects.filter(customer=customer)
        .prefetch_related("order_items__item", "customer__user")
        .order_by("-start_time")
    )

    serializer = OrderSerializer(orders, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
