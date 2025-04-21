from django.utils.timezone import make_aware
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from ..models.order_models import Order
from rest_framework.permissions import IsAuthenticated
from datetime import datetime


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def daily_stats(request):
    if not hasattr(request.user, "restaurant"):
        return Response({"error": "Only restaurant accounts can access this."}, status=403)

    restaurant = request.user.restaurant
    date_str = request.query_params.get("date")

    if not date_str:
        return Response({"error": "Date is required"}, status=400)

    try:
        target_date = datetime.strptime(date_str, "%Y-%m-%d")
        start = make_aware(datetime.combine(target_date, datetime.min.time()))
        end = make_aware(datetime.combine(target_date, datetime.max.time()))
    except ValueError:
        return Response({"error": "Invalid date format"}, status=400)

    orders = Order.objects.filter(
        restaurant=restaurant,
        start_time__range=(start, end)
    )

    total_orders = orders.count()
    total_sales = sum(order.total_price for order in orders)
    avg_order_value = total_sales / total_orders if total_orders else 0
    active_bartenders = (
        orders.exclude(worker=None)
        .values_list("worker_id", flat=True)
        .distinct()
        .count()
    )

    return Response({
        "total_orders": total_orders,
        "total_sales": round(total_sales, 2),
        "avg_order_value": round(avg_order_value, 2),
        "active_bartenders": active_bartenders,
    })