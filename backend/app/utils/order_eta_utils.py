# app/utils/order_eta_utils.py

from datetime import timedelta

from app.models.order_models import Order
from app.scheduler_instance import get_restaurant_scheduler
from app.utils.eta_calculator import (
    calculate_beverage_eta_multibartender,
    calculate_food_eta,
    round_to_nearest_five,
)
from django.utils import timezone


def recalculate_pending_etas(restaurant_id, num_bartenders=2):
    """
    Recalculate and persist, for each pending order:
      - estimated_food_ready_time  (or None)
      - estimated_beverage_ready_time  (or None)
      - food_eta_minutes  (or None)
      - beverage_eta_minutes  (or None)
    """
    # Use a single “now” floored to the minute
    now = timezone.now().replace(second=0, microsecond=0)

    # Fresh scheduler for this restaurant
    scheduler = get_restaurant_scheduler(restaurant_id, num_bartenders)
    scheduler.schedulers = [type(s)() for s in scheduler.schedulers]

    pending = (
        Order.objects
        .filter(restaurant_id=restaurant_id, status="pending")
        .order_by("start_time")
    )

    for order in pending:
        # Count food vs. beverage items
        num_food = sum(
            oi.quantity
            for oi in order.order_items.all()
            if oi.item.category.lower() != "beverage"
        )
        num_bev = sum(
            oi.quantity
            for oi in order.order_items.all()
            if oi.item.category.lower() == "beverage"
        )

        # — FOOD ETA —
        if num_food > 0:
            # Round to nearest 5 minutes
            food_mins = round_to_nearest_five(calculate_food_eta(num_food))
            food_dt = now + timedelta(minutes=food_mins)
            order.estimated_food_ready_time = food_dt
            order.food_eta_minutes = food_mins
        else:
            order.estimated_food_ready_time = None
            order.food_eta_minutes = None

        # — BEVERAGE ETA —
        if num_bev > 0:
            # Compute exact finish, then floor to minute
            _, bev_finish_dt, bart_idx = calculate_beverage_eta_multibartender(
                num_bev, now, scheduler
            )
            bev_finish_dt = bev_finish_dt.replace(second=0, microsecond=0)
            order.estimated_beverage_ready_time = bev_finish_dt

            # Delta in whole minutes
            bev_mins = int((bev_finish_dt - now).total_seconds() / 60)
            order.beverage_eta_minutes = bev_mins

            # Mark that bartender slot taken
            slot_start = bev_finish_dt - timedelta(minutes=num_bev)
            scheduler.add_order_to_bartender(bart_idx, slot_start, num_bev)
        else:
            order.estimated_beverage_ready_time = None
            order.beverage_eta_minutes = None

        # Persist both timestamps and minute‐deltas
        order.save(update_fields=[
            "estimated_food_ready_time",
            "estimated_beverage_ready_time",
            "food_eta_minutes",
            "beverage_eta_minutes",
        ])
