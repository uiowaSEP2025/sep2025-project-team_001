from app.scheduler_instance import get_restaurant_scheduler
from app.utils.eta_calculator import calculate_overall_eta
from django.utils import timezone
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

        # --- ETA Calculation Integration ---

        # 1. Count the food and beverage items. We assume that items with category "beverage"
        #    are beverages, and all others are food.
        num_food_items = 0
        num_beverage_items = 0
        for order_item in order.order_items.all():
            # Assume that the category field is available and non-null.
            if order_item.item.category and order_item.item.category.lower() == "beverage":
                num_beverage_items += order_item.quantity
            else:
                num_food_items += order_item.quantity

        # 2. Retrieve the correct scheduler for this restaurant.
        restaurant_id = order.restaurant.id
        # You can adjust the number of bartenders as needed.
        scheduler = get_restaurant_scheduler(restaurant_id, num_bartenders=2)

        # 3. Calculate the overall ETA using our utility function.
        now = timezone.now()
        overall_eta = calculate_overall_eta(
            num_food_items,
            num_beverage_items,
            now,
            scheduler
        )

        # 4. Set the estimated pickup time based on the ETA.
        order.estimated_pickup_time = now + timezone.timedelta(minutes=overall_eta)
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
def update_order_status(request, order_id, new_status):
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
        order = Order.objects.get(pk=order_id, restaurant=request.user.restaurant)
    except Order.DoesNotExist:
        return Response({"error": "Order not found."}, status=status.HTTP_404_NOT_FOUND)

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


@api_view(["POST"])
def estimate_order_eta(request):
    """
    Given a list of order_items (with item_id and quantity) and restaurant_id,
    return the ASAP estimated pickup time without creating an order.
    """
    data = request.data
    restaurant_id = data.get("restaurant_id")
    order_items = data.get("order_items")

    if restaurant_id is None or order_items is None:
        return Response(
            {"error": "restaurant_id and order_items are required."},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Count food vs. beverage
    num_food = 0
    num_bev = 0
    # Bulk-fetch items to minimize queries
    from app.models.restaurant_models import Item
    items = Item.objects.in_bulk([oi["item_id"] for oi in order_items])
    for oi in order_items:
        item = items.get(oi["item_id"])
        qty = oi.get("quantity", 0) or 0
        if not item:
            return Response({"error": f"Invalid item_id {oi['item_id']}"}, status=400)
        if item.category and item.category.lower() == "beverage":
            num_bev += qty
        else:
            num_food += qty

    # Scheduler for this restaurant (does not mutate its state)
    scheduler = get_restaurant_scheduler(restaurant_id, num_bartenders=2)

    # Calculate ETA using real clock time
    now = timezone.now()
    eta_minutes = calculate_overall_eta(num_food, num_bev, now, scheduler)

    # Return both minutes and a human time
    pickup_time = now + timezone.timedelta(minutes=eta_minutes)
    return Response({
        "eta_minutes": eta_minutes,
        "estimated_pickup_time": pickup_time.isoformat()
    })
