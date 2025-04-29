from django.utils.timezone import make_aware
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from ..models.order_models import Order
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from ..models.worker_models import Worker
from django.db.models import Avg, Min, Max, Sum, F, ExpressionWrapper, DurationField
from ..models.restaurant_models import Item


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
        orders = Order.objects.filter(
            worker=worker,
            status='completed',
            start_time__isnull=False,
            completion_time__isnull=False
        ).annotate(
            elapsed_time=ExpressionWrapper(
                F('completion_time') - F('start_time'),
                output_field=DurationField()
            )
        )

        total_orders = orders.count()

        if total_orders == 0:
            stats.append({
                "worker_name": worker.name,
                "role": worker.role,
                "total_orders": 0,
                "average_time_seconds": None,
                "fastest_time_seconds": None,
                "slowest_time_seconds": None,
                "total_sales": 0.0,
            })
            continue

        aggregates = orders.aggregate(
            avg_time=Avg('elapsed_time'),
            fastest=Min('elapsed_time'),
            slowest=Max('elapsed_time'),
            total_sales=Sum('total_price')
        )

        stats.append({
            "worker_name": worker.name,
            "role": worker.role,
            "total_orders": total_orders,
            "average_time_seconds": aggregates['avg_time'].total_seconds() if aggregates['avg_time'] else None,
            "fastest_time_seconds": aggregates['fastest'].total_seconds() if aggregates['fastest'] else None,
            "slowest_time_seconds": aggregates['slowest'].total_seconds() if aggregates['slowest'] else None,
            "total_sales": float(aggregates['total_sales']) if aggregates['total_sales'] else 0.0,
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
        .order_by("-times_ordered")
        .values("name", "price", "times_ordered")
    )

    return Response({"items": list(items)}, status=200)