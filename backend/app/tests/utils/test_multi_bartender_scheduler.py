# app/tests/utils/test_multi_bartender_scheduler.py

import pytest
from datetime import timedelta
from app.utils.multi_bartender_scheduler import MultiBartenderScheduler
from django.utils import timezone


@pytest.fixture
def multi_scheduler():
    # Create a MultiBartenderScheduler instance with 2 bartenders.
    return MultiBartenderScheduler(num_bartenders=2)


def test_find_best_free_slot_initial(multi_scheduler):
    now = timezone.now()
    free_start, bartender_index = multi_scheduler.find_best_free_slot(now, 5)
    assert free_start == now
    assert bartender_index in [0, 1]


def test_find_best_free_slot_one_busy(multi_scheduler):
    now = timezone.now()
    multi_scheduler.schedulers[0].add_order(now, 10)
    free_start, bartender_index = multi_scheduler.find_best_free_slot(now, 5)
    assert free_start == now
    assert bartender_index == 1


def test_find_best_free_slot_with_offset(multi_scheduler):
    now = timezone.now()
    multi_scheduler.schedulers[0].add_order(now + timedelta(minutes=5), 10)
    free_start, bartender_index = multi_scheduler.find_best_free_slot(now, 5)
    assert free_start == now


def test_add_order_then_free_slot(multi_scheduler):
    now = timezone.now()
    free_start, bartender_index = multi_scheduler.find_best_free_slot(now, 5)
    multi_scheduler.add_order_to_bartender(bartender_index, free_start, 5)
    updated_free = multi_scheduler.schedulers[bartender_index].find_free_slot(now, 5)
    assert updated_free == free_start + timedelta(minutes=5)


def test_multiple_orders_across_bartenders(multi_scheduler):
    now = timezone.now()
    multi_scheduler.schedulers[0].add_order(now, 10)
    free_start, bartender_index = multi_scheduler.find_best_free_slot(now, 5)
    assert free_start == now
    assert bartender_index == 1

    multi_scheduler.schedulers[1].add_order(now, 5)
    free_start, bartender_index = multi_scheduler.find_best_free_slot(now, 5)
    assert free_start == now + timedelta(minutes=5)
    assert bartender_index in [0, 1]


def test_overlapping_orders(multi_scheduler):
    now = timezone.now()
    multi_scheduler.schedulers[0].add_order(now, 10)
    multi_scheduler.schedulers[1].add_order(now + timedelta(minutes=5), 10)
    free_start, bartender_index = multi_scheduler.find_best_free_slot(now, 5)
    assert free_start == now + timedelta(minutes=10)
    assert bartender_index == 0


def test_exact_fit_slot(multi_scheduler):
    now = timezone.now()
    # Bartender 0 has a 5‑min gap at t+10→t+15, but bartender 1 is free at t=now.
    multi_scheduler.schedulers[0].add_order(now, 10)
    multi_scheduler.schedulers[0].add_order(now + timedelta(minutes=15), 5)
    free_start, bartender_index = multi_scheduler.find_best_free_slot(now, 5)
    assert free_start == now
    assert bartender_index == 1
