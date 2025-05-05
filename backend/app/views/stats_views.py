import json
from datetime import datetime

from django.core.serializers.json import DjangoJSONEncoder
from django.db.models import (
    Avg,
    DurationField,
    ExpressionWrapper,
    F,
    FloatField,
    Max,
    Min,
    Sum,
)
from django.db.models.functions import Trunc
from django.utils.timezone import make_aware, now, timedelta
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from ..models.order_models import Order
from ..models.restaurant_models import Item
from ..models.worker_models import Worker


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
        start_time__range=(start, end),
        status__in=["completed", "picked_up"]
    )

    total_orders = orders.count()
    total_sales = sum(order.total_price for order in orders)
    avg_order_value = total_sales / total_orders if total_orders else 0
    active_workers = (
        orders.exclude(worker=None)
        .values_list("worker_id", flat=True)
        .distinct()
        .count()
    )

    return Response({
        "total_orders": total_orders,
        "total_sales": round(total_sales, 2),
        "avg_order_value": round(avg_order_value, 2),
        "active_workers": active_workers,
    })


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_bartender_statistics(request):
    if not hasattr(request.user, "restaurant"):
        return Response({"error": "Only restaurant accounts can access bartender statistics."}, status=403)

    restaurant = request.user.restaurant
    workers = Worker.objects.filter(restaurant=restaurant)
    stats = []

    for worker in workers:
        # All completed orders with start and end time
        orders = Order.objects.filter(
            worker=worker,
            status__in=["completed", "picked_up"],
            start_time__isnull=False,
            completion_time__isnull=False,
        ).annotate(
            duration=ExpressionWrapper(
                F('completion_time') - F('start_time'),
                output_field=DurationField()
            )
        )

        total_orders = orders.count()
        total_sales = orders.aggregate(total=Sum('total_price'))['total'] or 0
        aggregates = orders.aggregate(
            avg_duration=Avg('duration'),
            min_duration=Min('duration'),
            max_duration=Max('duration'),
        )

        stats.append({
            "worker_name": worker.name,
            "role": worker.role,
            "total_orders": total_orders,
            "average_time_seconds": aggregates["avg_duration"].total_seconds() if aggregates["avg_duration"] else None,
            "fastest_time_seconds": aggregates["min_duration"].total_seconds() if aggregates["min_duration"] else None,
            "slowest_time_seconds": aggregates["max_duration"].total_seconds() if aggregates["max_duration"] else None,
            "total_sales": float(total_sales),
        })

    return Response({"bartender_statistics": stats})


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_item_statistics(request):
    if not hasattr(request.user, "restaurant"):
        return Response({"error": "Unauthorized"}, status=403)

    restaurant = request.user.restaurant

    items = (
        Item.objects.filter(restaurant=restaurant)
        .annotate(
            sales=ExpressionWrapper(
                F("price") * F("times_ordered"),
                output_field=FloatField()
            ),
            avg_rating=Avg("orderitem__order__review__rating")
        )
        .order_by("-times_ordered")
        .values("name", "price", "times_ordered", "sales", "avg_rating")
    )

    return Response({"items": list(items)}, status=200)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_restaurant_statistics(request):
    if not hasattr(request.user, "restaurant"):
        return Response({"error": "Only restaurant accounts can access this."}, status=403)

    restaurant = request.user.restaurant
    range_param = request.query_params.get("range", "week")

    # Determine time window
    today = now()
    if range_param == "day":
        start_time = today - timedelta(days=1)
        interval = "hour"
    elif range_param == "week":
        start_time = today - timedelta(weeks=1)
        interval = "day"
    elif range_param == "month":
        start_time = today - timedelta(days=30)
        interval = "day"
    elif range_param == "year":
        start_time = make_aware(datetime(today.year, 1, 1))
        interval = "month"

    trunc_fn = {
        "hour": Trunc("start_time", "hour"),
        "day": Trunc("start_time", "day"),
        "week": Trunc("start_time", "week"),
        "month": Trunc("start_time", "month"),
    }[interval]

    data = (
        Order.objects.filter(restaurant=restaurant, start_time__gte=start_time, status__in=["completed", "picked_up"])
        .annotate(period=trunc_fn)
        .values("period")
        .annotate(total_sales=Sum("total_price"))
        .order_by("period")
    )

    return Response(json.loads(json.dumps(list(data), cls=DjangoJSONEncoder)))
