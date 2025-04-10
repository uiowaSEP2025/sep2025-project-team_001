from datetime import timedelta

import pytest
from app.utils.multi_bartender_scheduler import MultiBartenderScheduler
from django.utils import timezone


@pytest.fixture
def multi_scheduler():
    # Create a MultiBartenderScheduler instance with 2 bartenders.
    return MultiBartenderScheduler(num_bartenders=2)


def test_find_best_free_slot_initial(multi_scheduler):
    """
    With no orders scheduled, the earliest free slot should be the current time
    for any bartender.
    """
    now = timezone.now()
    free_start, bartender_index = multi_scheduler.find_best_free_slot(now, 5)
    assert free_start == now
    assert bartender_index in [0, 1]


def test_find_best_free_slot_one_busy(multi_scheduler):
    """
    Mark bartender 0 as busy from now to now+10 minutes.
    For a required 5-minute slot starting at now, the scheduler should choose bartender 1.
    """
    now = timezone.now()
    multi_scheduler.schedulers[0].add_order(now, 10)
    free_start, bartender_index = multi_scheduler.find_best_free_slot(now, 5)
    assert free_start == now
    assert bartender_index == 1


def test_find_best_free_slot_with_offset(multi_scheduler):
    """
    With a busy interval on one bartender and different current time,
    the scheduler should compute the earliest available slot properly.
    """
    now = timezone.now()
    # Bartender 0 busy from now+5 to now+15
    multi_scheduler.schedulers[0].add_order(now + timedelta(minutes=5), 10)
    free_start, bartender_index = multi_scheduler.find_best_free_slot(now, 5)
    # A 5-minute slot fits before the busy window
    assert free_start == now


def test_add_order_then_free_slot(multi_scheduler):
    """
    After scheduling an order on a specific bartender, the free slot for that bartender
    should update accordingly.
    """
    now = timezone.now()
    free_start, bartender_index = multi_scheduler.find_best_free_slot(now, 5)
    multi_scheduler.add_order_to_bartender(bartender_index, free_start, 5)
    # Now, the next free slot for that bartender should be free_start + 5 minutes
    updated_free = multi_scheduler.schedulers[bartender_index].find_free_slot(now, 5)
    assert updated_free == free_start + timedelta(minutes=5)


def test_multiple_orders_across_bartenders(multi_scheduler):
    """
    Schedule orders on both bartenders and verify that the scheduler finds the earliest available slot.
    """
    now = timezone.now()
    # Bartender 0 busy from now to now+10
    multi_scheduler.schedulers[0].add_order(now, 10)
    free_start, bartender_index = multi_scheduler.find_best_free_slot(now, 5)
    assert free_start == now
    assert bartender_index == 1

    # Now, mark bartender 1 busy from now to now+5
    multi_scheduler.schedulers[1].add_order(now, 5)
    free_start, bartender_index = multi_scheduler.find_best_free_slot(now, 5)
    # Bartender 1 is free at now+5, bartender 0 at now+10 → best is now+5
    assert free_start == now + timedelta(minutes=5)
    assert bartender_index in [0, 1]
