# app/utils/eta_calculator.py

import math


def round_to_nearest_five(minutes):
    """Round up minutes to the nearest multiple of 5."""
    return math.ceil(minutes / 5) * 5


def calculate_food_eta(num_food_items, base_time=15, additional_time_per_item=2):
    """Calculate food ETA."""
    return base_time + (additional_time_per_item * num_food_items)


def calculate_beverage_eta(num_beverage_items, beverage_time_per_item=1, bartender_queue_delay=0):
    """
    Calculate beverage ETA in a simplified scenario.
    This is just used when not scheduling dynamically.
    """
    return bartender_queue_delay + (beverage_time_per_item * num_beverage_items)


def calculate_beverage_eta_multibartender(num_beverage_items, current_time, multi_scheduler, beverage_time_per_item=1):
    """
    Calculate beverage ETA using multi-bartender scheduling.

    :param num_beverage_items: Number of beverages in the order.
    :param current_time: Current time in minutes (from your reference time).
    :param multi_scheduler: An instance of MultiBartenderScheduler.
    :param beverage_time_per_item: Preparation time per beverage.
    :return: A tuple (beverage_eta, assigned_bartender_index) where beverage_eta is in minutes.
    """
    required_duration = num_beverage_items * beverage_time_per_item
    free_start_time, bartender_index = multi_scheduler.find_best_free_slot(current_time, required_duration)
    finish_time = free_start_time + required_duration
    # The ETA is the time from current_time to the finish time.
    beverage_eta = finish_time - current_time
    return beverage_eta, bartender_index


def calculate_overall_eta(num_food_items, num_beverage_items, current_time, multi_scheduler, beverage_time_per_item=1):
    """
    Calculate overall ETA given food and beverage orders.

    The overall ETA is the maximum between the food ETA and the scheduled beverage ETA,
    rounded up to the nearest 5 minutes.
    """
    food_eta = calculate_food_eta(num_food_items)
    beverage_eta, _ = calculate_beverage_eta_multibartender(num_beverage_items, current_time, multi_scheduler,
                                                      beverage_time_per_item)
    overall_eta = max(food_eta, beverage_eta)
    return round_to_nearest_five(overall_eta)
