from django.utils.timezone import make_aware
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from ..models.order_models import Order
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from ..models.worker_models import Worker
from django.db.models import Avg, Min, Max, Sum, F, ExpressionWrapper, DurationField


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
def get_bartender_statistics(request, worker_id):
    try:
        worker = Worker.objects.get(pk=worker_id)
    except Worker.DoesNotExist:
        return Response({"error": "Worker not found"}, status=404)

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

    # If no orders then don't query database
    if total_orders == 0:
        return Response({
            "total_orders": 0,
            "average_time_seconds": None,
            "fastest_time_seconds": None,
            "slowest_time_seconds": None,
            "total_sales": 0.0,
        })

    aggregates = orders.aggregate(
        avg_time=Avg('elapsed_time'),
        fastest=Min('elapsed_time'),
        slowest=Max('elapsed_time'),
        total_sales=Sum('total_price')
    )

    average_time = aggregates['avg_time']
    fastest_time = aggregates['fastest']
    slowest_time = aggregates['slowest']
    total_sales = aggregates['total_sales']

    return Response({
        "total_orders": total_orders,
        "average_time_seconds": average_time.total_seconds() if average_time else None,
        "fastest_time_seconds": fastest_time.total_seconds() if fastest_time else None,
        "slowest_time_seconds": slowest_time.total_seconds() if slowest_time else None,
        "total_sales": float(total_sales) if total_sales else 0.0,
    })