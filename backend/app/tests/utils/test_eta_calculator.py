# app/tests/utils/test_eta_calculator.py


import pytest
from app.utils.eta_calculator import (
    calculate_beverage_eta_multibartender,
    calculate_food_eta,
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
    assert round_to_nearest_five(0) == 0
    assert round_to_nearest_five(-3) == 0  # Negative values round up to 0


def test_calculate_food_eta():
    # For 3 food items: 15 + (2*3) = 21 minutes.
    assert calculate_food_eta(3) == 21
    # For 0 food items: base time only.
    assert calculate_food_eta(0) == 15
    # For a large number of food items.
    assert calculate_food_eta(100) == 215


def test_calculate_beverage_eta_multibartender_no_orders(multi_scheduler):
    now = timezone.now()
    # With no orders scheduled, 2 beverages require 2 minutes total.
    beverage_eta, finish_dt, bartender_idx = calculate_beverage_eta_multibartender(2, now, multi_scheduler)
    assert beverage_eta == 2
    # Bartender index can be either 0 or 1.
    assert bartender_idx in [0, 1]


def test_calculate_beverage_eta_multibartender_with_existing_order(multi_scheduler):
    now = timezone.now()
    # Simulate that bartender 0 is busy from now to now+10.
    multi_scheduler.schedulers[0].add_order(now, 10)
    # With 2 beverages (2 min duration), should pick bartender 1 at time 0.
    beverage_eta, finish_dt, bartender_idx = calculate_beverage_eta_multibartender(2, now, multi_scheduler)
    assert beverage_eta == 2
    assert bartender_idx == 1


def test_calculate_beverage_eta_multibartender_with_overlapping_orders(multi_scheduler):
    now = timezone.now()
    # Both bartenders busy right now for 10 minutes:
    multi_scheduler.schedulers[0].add_order(now, 10)
    multi_scheduler.schedulers[1].add_order(now, 10)
    # Now the earliest free slot is at t+10 on bartender 0 → ETA = 10 + 2 = 12.
    beverage_eta, finish_dt, bartender_idx = calculate_beverage_eta_multibartender(2, now, multi_scheduler)
    assert beverage_eta == 12
    assert bartender_idx == 0
