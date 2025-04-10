import pytest
from app.utils.eta_calculator import (
    calculate_beverage_eta,
    calculate_beverage_eta_multibartender,
    calculate_food_eta,
    calculate_overall_eta,
    round_to_nearest_five,
)
from app.utils.multi_bartender_scheduler import MultiBartenderScheduler
from django.utils import timezone


@pytest.fixture
def multi_scheduler():
    # Create a multi-bartender scheduler with 2 bartenders.
    return MultiBartenderScheduler(num_bartenders=2)


def test_round_to_nearest_five():
    assert round_to_nearest_five(21) == 25
    assert round_to_nearest_five(20) == 20
    assert round_to_nearest_five(1) == 5


def test_calculate_food_eta():
    # For 3 food items: 15 + (2*3) = 21 minutes.
    assert calculate_food_eta(3) == 21


def test_calculate_beverage_eta():
    # Simplified calculation: with 2 beverages at 1 minute each and no delay.
    assert calculate_beverage_eta(2) == 2
    # With a delay of 5 minutes in the bartender queue.
    assert calculate_beverage_eta(2, beverage_time_per_item=1, bartender_queue_delay=5) == 7


def test_calculate_beverage_eta_multibartender_no_orders(multi_scheduler):
    now = timezone.now()
    # With no orders scheduled, 2 beverages require 2 minutes total.
    beverage_eta, bartender_idx = calculate_beverage_eta_multibartender(2, now, multi_scheduler)
    assert beverage_eta == 2
    # Bartender index can be either 0 or 1.
    assert bartender_idx in [0, 1]


def test_calculate_beverage_eta_multibartender_with_existing_order(multi_scheduler):
    now = timezone.now()
    # Simulate that bartender 0 is busy from 0 to 10.
    multi_scheduler.schedulers[0].add_order(now, 10)
    # With 2 beverages (duration 2 minutes needed), bartender 0 is busy so scheduler should pick bartender 1.
    beverage_eta, bartender_idx = calculate_beverage_eta_multibartender(2, now, multi_scheduler)
    assert beverage_eta == 2  # Since bartender 1 is free at time 0.
    assert bartender_idx == 1


def test_calculate_overall_eta_beverage_less_than_food(multi_scheduler):
    now = timezone.now()
    # 3 food items => food ETA = 15 + (2*3) = 21.
    # 1 beverage => beverage ETA (with no delay) = 1.
    # Overall ETA should be max(21,1)=21 rounded to nearest 5 = 25.
    overall_eta = calculate_overall_eta(3, 1, now, multi_scheduler)
    assert overall_eta == 25


def test_calculate_overall_eta_beverage_greater(multi_scheduler):
    now = timezone.now()
    # 1 food item => food ETA = 15 + 2 = 17.
    # 10 beverages => required duration = 10 minutes.
    # Simulate both bartenders busy until 10 minutes:
    multi_scheduler.schedulers[0].add_order(now, 10)
    multi_scheduler.schedulers[1].add_order(now, 10)
    # Now, both bartenders are free at 10, so beverage ETA = 10 (free slot) + 10 (duration) - 0 = 20.
    # Overall ETA becomes max(17, 20) = 20 (already a multiple of 5).
    overall_eta = calculate_overall_eta(1, 10, now, multi_scheduler)
    assert overall_eta == 20
