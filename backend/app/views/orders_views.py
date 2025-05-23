from datetime import timedelta

from app.mobileViews.utils import send_fcm_httpv1, send_notification_to_device
from app.scheduler_instance import get_restaurant_scheduler
from app.utils.eta_calculator import (
    calculate_beverage_eta_multibartender,
    calculate_food_eta,
    round_to_nearest_five,
)
from app.utils.order_eta_utils import recalculate_pending_etas
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models import Item, Restaurant
from ..models.order_models import Order
from ..models.worker_models import Worker
from ..serializers.order_serializer import OrderSerializer


@api_view(["POST"])
def create_order(request):
    serializer = OrderSerializer(data=request.data)
    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 1) Persist the order & items, then set total_price
    order = serializer.save()
    order.total_price = order.get_total()
    order.save(update_fields=["total_price"])

    # Recalculate ETAs
    recalculate_pending_etas(order.restaurant.id)
    order.refresh_from_db()

    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def retrieve_active_orders(request):
    if not hasattr(request.user, "restaurant"):
        return Response(
            {"error": "Only restaurant accounts can view active orders."},
            status=status.HTTP_403_FORBIDDEN,
        )

    restaurant = request.user.restaurant
    statuses = request.GET.get("statuses")
    limit = int(request.GET.get("limit", 20))
    offset_raw = request.GET.get("offset")
    offset = int(offset_raw) if offset_raw is not None else None

    orders = Order.objects.filter(restaurant=restaurant)

    if statuses:
        status_list = [s.strip() for s in statuses.split(",") if s.strip()]
        if status_list:
            orders = orders.filter(status__in=status_list)

    orders = orders.order_by("-start_time")
    total = orders.count()

    if offset is not None:
        paginated_orders = orders[offset:offset + limit]
        next_offset = offset + limit if offset + limit < total else None
    else:
        paginated_orders = orders[:limit]
        next_offset = limit if limit < total else None

    serializer = OrderSerializer(paginated_orders, many=True)
    return Response({
        "results": serializer.data,
        "total": total,
        "next_offset": next_offset,
    }, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_order_status(request, restaurant_id, order_id, new_status):
    if not hasattr(request.user, "restaurant"):
        return Response(
            {"error": "Only restaurant accounts can update orders."},
            status=status.HTTP_403_FORBIDDEN,
        )

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
            order.start_time = timezone.now()
        except Worker.DoesNotExist:
            return Response({"error": "Worker not found."}, status=status.HTTP_404_NOT_FOUND)
        order.food_status = "in_progress"
        order.beverage_status = "in_progress"

    order.status = normalized_status
    order.save()

    if order.customer.fcm_token:
        send_fcm_httpv1(
            device_token=order.customer.fcm_token,
            title="Order Update",
            body=f"Your order #{order.id} is now {order.status}",
            data={"type": "ORDER_UPDATE", "order_id": str(order.id)}
        )

        send_notification_to_device(
            device_token=order.customer.fcm_token,
            title="Order Update",
            body=f"Your order #{order.id} is now {order.status}",
            data={"type": "ORDER_UPDATE", "order_id": str(order.id)}
        )

    recalculate_pending_etas(order.restaurant.id)
    order.refresh_from_db()
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["PATCH"])
@permission_classes([IsAuthenticated])
def update_order_category_status(request, restaurant_id, order_id, category, new_status):
    if not hasattr(request.user, "restaurant"):
        return Response(
            {"error": "Only restaurant accounts can update orders."},
            status=status.HTTP_403_FORBIDDEN,
        )

    normalized_category = category.lower()
    normalized_status = new_status.lower().replace(" ", "_")

    if normalized_category not in ["food", "beverage"]:
        return Response({"error": "Invalid category"}, status=status.HTTP_400_BAD_REQUEST)

    if normalized_status not in ["completed", "picked_up"]:
        return Response({"error": f"Invalid status '{new_status}'"}, status=status.HTTP_400_BAD_REQUEST)

    try:
        restaurant = Restaurant.objects.get(pk=restaurant_id)
    except Restaurant.DoesNotExist:
        return Response({"error": "Restaurant not found."}, status=status.HTTP_404_NOT_FOUND)

    try:
        order = Order.objects.get(pk=order_id, restaurant=restaurant)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

    # Update food or beverage status
    if normalized_category == "food":
        order.food_status = normalized_status
    else:
        order.beverage_status = normalized_status

    # Determine correct main order status based on available categories
    status_priority = {"pending": 0, "in_progress": 1, "completed": 2, "picked_up": 3}
    reverse_lookup = {v: k for k, v in status_priority.items()}

    has_food = order.order_items.filter(item__category__iexact="food").exists()
    has_bev = order.order_items.filter(item__category__iexact="beverage").exists()

    food_val = status_priority[order.food_status] if has_food else None
    bev_val = status_priority[order.beverage_status] if has_bev else None

    if order.customer.fcm_token:
        send_fcm_httpv1(
            device_token=order.customer.fcm_token,
            title="Order Update",
            body=f"Your order #{order.id} is now {order.status}",
            data={"type": "ORDER_UPDATE", "order_id": str(order.id)}
        )

        send_notification_to_device(
            device_token=order.customer.fcm_token,
            title="Order Update",
            body=f"Your order #{order.id} is now {order.status}",
            data={"type": "ORDER_UPDATE", "order_id": str(order.id)}
        )

    if food_val is not None and bev_val is not None:
        min_val = min(food_val, bev_val)
    elif food_val is not None:
        min_val = food_val
    elif bev_val is not None:
        min_val = bev_val
    else:
        min_val = status_priority["pending"]

    order.status = reverse_lookup[min_val]
    order.save()

    if order.status == "completed":
        order.completion_time = timezone.now()
        order.save(update_fields=["completion_time"])

        for order_item in order.order_items.all():
            order_item.item.times_ordered += order_item.quantity
            order_item.item.save()

    #     order.refresh_from_db()
    #     serializer = OrderSerializer(order)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    return Response({
        "message": f"{normalized_category.capitalize()} status updated to '{normalized_status}'.",
        "order_id": order.id,
        "status": order.status,
        "food_status": order.food_status,
        "beverage_status": order.beverage_status,
        "completion_time": order.completion_time.isoformat() if order.completion_time else None,
    }, status=status.HTTP_200_OK)


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


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_order(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
    except:
        return Response(
            {"error": "Order not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    serializer = OrderSerializer(order)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def estimate_order_eta(request):
    data = request.data
    order_items = data.get("order_items")
    restaurant_id = data.get("restaurant_id")

    if restaurant_id is None or order_items is None:
        return Response(
            {"error": "restaurant_id and order_items are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # 1) Count food vs. beverage
    num_food = 0
    num_bev = 0
    items = Item.objects.in_bulk([oi["item_id"] for oi in order_items])
    for oi in order_items:
        item = items.get(oi["item_id"])
        qty = oi.get("quantity", 0) or 0
        if not item:
            return Response(
                {"error": f"Invalid item_id {oi['item_id']}"},
                status=status.HTTP_400_BAD_REQUEST
            )
        if item.category and item.category.lower() == "beverage":
            num_bev += qty
        else:
            num_food += qty

    # Prepare scheduler (does not mutate its state for this estimate)
    scheduler = get_restaurant_scheduler(restaurant_id, num_bartenders=1)

    now = timezone.now()

    # 2) Food ETA: simple formula
    raw_food = calculate_food_eta(num_food)
    food_eta = round_to_nearest_five(raw_food)
    food_ready = now + timedelta(minutes=food_eta)

    # 3) Beverage ETA: scheduler‐based
    raw_bev, bev_finish_dt, bartender_idx = calculate_beverage_eta_multibartender(
        num_bev, now, scheduler
    )
    bev_eta = round_to_nearest_five(raw_bev)
    bev_ready = now + timedelta(minutes=bev_eta)

    return Response({
        "food_eta_minutes": food_eta,
        "beverage_eta_minutes": bev_eta,
        "estimated_food_ready_time": food_ready.isoformat(),
        "estimated_beverage_ready_time": bev_ready.isoformat(),
    }, status=status.HTTP_200_OK)
