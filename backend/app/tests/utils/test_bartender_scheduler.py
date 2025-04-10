import pytest

from app.utils.bartender_scheduler import BartenderScheduler


@pytest.fixture
def scheduler():
    return BartenderScheduler()


def test_find_free_slot_no_orders(scheduler):
    # With no orders, free slot is the current time.
    assert scheduler.find_free_slot(0, 5) == 0
    assert scheduler.find_free_slot(10, 3) == 10


def test_find_free_slot_with_one_order(scheduler):
    # Schedule an order from 10 to 15 minutes.
    scheduler.add_order(10, 5)  # Order occupies [10, 15)
    # A 5-minute slot starting at 0 should be available before the busy interval.
    assert scheduler.find_free_slot(0, 5) == 0
    # If current_time is 10, the busy interval makes it unavailable, so slot should start after 15.
    assert scheduler.find_free_slot(10, 5) == 15


def test_find_free_slot_with_gap(scheduler):
    # Schedule an order from 10 to 15 minutes.
    scheduler.add_order(10, 5)
    # For a required duration of 3 minutes, there is a free slot before 10.
    assert scheduler.find_free_slot(0, 3) == 0
    # For a required duration of 10 minutes, the free slot must start after the busy period.
    assert scheduler.find_free_slot(0, 10) == 15


def test_back_to_back_orders(scheduler):
    # Schedule two orders back-to-back.
    scheduler.add_order(0, 10)  # Occupies 0 to 10.
    scheduler.add_order(10, 10)  # Occupies 10 to 20.
    # With no gap in between, a new 5-minute slot should start at 20.
    assert scheduler.find_free_slot(0, 5) == 20
    # If current_time is 5 (within the busy interval), it should also return 20.
    assert scheduler.find_free_slot(5, 5) == 20
