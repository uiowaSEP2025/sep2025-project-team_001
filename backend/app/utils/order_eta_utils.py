# app/utils/order_eta_utils.py

from datetime import timedelta

from django.utils import timezone

from app.models.order_models import Order
from app.scheduler_instance import get_restaurant_scheduler
from app.utils.eta_calculator import (
    calculate_food_eta,
    calculate_beverage_eta_multibartender,
    round_to_nearest_five,
)


def recalculate_pending_etas(restaurant_id, num_bartenders=2):
    now = timezone.now().replace(second=0, microsecond=0)

    # fresh scheduler
    scheduler = get_restaurant_scheduler(restaurant_id, num_bartenders)
    scheduler.schedulers = [type(s)() for s in scheduler.schedulers]

    pending = (
        Order.objects
        .filter(restaurant_id=restaurant_id, status="pending")
        .order_by("start_time")
    )

    for order in pending:
        # count items
        num_food = sum(
            oi.quantity for oi in order.order_items.all()
            if oi.item.category.lower() != "beverage"
        )
        num_bev = sum(
            oi.quantity for oi in order.order_items.all()
            if oi.item.category.lower() == "beverage"
        )

        # food ETA (rounded to nearest 5 minutes), then floored to minute
        food_mins = round_to_nearest_five(calculate_food_eta(num_food))
        order.estimated_food_ready_time = (now + timedelta(minutes=food_mins))

        # beverage ETA: get exact finish, then floor to minute
        _, bev_finish_dt, bart_idx = calculate_beverage_eta_multibartender(
            num_bev, now, scheduler
        )
        bev_finish_dt = bev_finish_dt.replace(second=0, microsecond=0)
        order.estimated_beverage_ready_time = bev_finish_dt

        order.save(update_fields=[
            "estimated_food_ready_time",
            "estimated_beverage_ready_time",
        ])

        # mark that slot taken
        if num_bev > 0:
            slot_start = bev_finish_dt - timedelta(minutes=num_bev)
            scheduler.add_order_to_bartender(bart_idx, slot_start, num_bev)
