from datetime import timedelta

import pytest
from app.utils.bartender_scheduler import BartenderScheduler
from django.utils import timezone


@pytest.fixture
def scheduler():
    return BartenderScheduler()


def test_find_free_slot_no_orders(scheduler):
    now = timezone.now()
    # With no orders, free slot is the current time.
    assert scheduler.find_free_slot(now, 5) == now
    later = now + timedelta(minutes=10)
    assert scheduler.find_free_slot(later, 3) == later


def test_find_free_slot_with_one_order(scheduler):
    now = timezone.now()
    # Schedule an order from now+10 to now+15.
    scheduler.add_order(now + timedelta(minutes=10), 5)
    # A slot starting at now should be available before that busy interval.
    assert scheduler.find_free_slot(now, 5) == now
    # If current_time is now+10, slot should start after busy period at now+15.
    assert scheduler.find_free_slot(now + timedelta(minutes=10), 5) == now + timedelta(minutes=15)


def test_find_free_slot_with_gap(scheduler):
    now = timezone.now()
    # Schedule an order from now+10 to now+15.
    scheduler.add_order(now + timedelta(minutes=10), 5)
    # For a 3-minute slot, free before busy interval:
    assert scheduler.find_free_slot(now, 3) == now
    # For a 10-minute slot, must start after busy period:
    assert scheduler.find_free_slot(now, 10) == now + timedelta(minutes=15)


def test_back_to_back_orders(scheduler):
    now = timezone.now()
    # Schedule two back-to-back: now→now+10, and now+10→now+20
    scheduler.add_order(now, 10)
    scheduler.add_order(now + timedelta(minutes=10), 10)
    # Next 5-minute slot should start at now+20
    assert scheduler.find_free_slot(now, 5) == now + timedelta(minutes=20)
    # If current_time is now+5 (within first busy interval), still returns now+20
    assert scheduler.find_free_slot(now + timedelta(minutes=5), 5) == now + timedelta(minutes=20)
