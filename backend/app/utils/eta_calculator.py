import math
from datetime import timedelta


def round_to_nearest_five(minutes):
    return math.ceil(minutes / 5) * 5


def calculate_food_eta(num_food_items, base_time=15, per_item=2):
    return base_time + per_item * num_food_items


def calculate_beverage_eta_multibartender(num_bev, now_dt, scheduler, per_bev=1):
    duration = num_bev * per_bev
    slot_start, idx = scheduler.find_best_free_slot(now_dt, duration)
    finish_dt = slot_start + timedelta(minutes=duration)
    eta = (finish_dt - now_dt).total_seconds() / 60
    return round(eta), finish_dt, idx
