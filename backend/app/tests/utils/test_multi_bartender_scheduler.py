import pytest
from app.utils.multi_bartender_scheduler import MultiBartenderScheduler


@pytest.fixture
def multi_scheduler():
    # Create a MultiBartenderScheduler instance with 2 bartenders.
    return MultiBartenderScheduler(num_bartenders=2)


def test_find_best_free_slot_initial(multi_scheduler):
    """
    With no orders scheduled, the earliest free slot should be the current time (0)
    for any bartender.
    """
    free_start, bartender_index = multi_scheduler.find_best_free_slot(0, 5)
    assert free_start == 0
    # Since both are free, the scheduler might choose either bartender.
    assert bartender_index in [0, 1]


def test_find_best_free_slot_one_busy(multi_scheduler):
    """
    Mark bartender 0 as busy from minute 0 to 10.
    For a required 5-minute slot starting at 0, the scheduler should choose bartender 1.
    """
    multi_scheduler.schedulers[0].add_order(0, 10)
    free_start, bartender_index = multi_scheduler.find_best_free_slot(0, 5)
    # Bartender 1 is free at time 0.
    assert free_start == 0
    assert bartender_index == 1


def test_find_best_free_slot_with_offset(multi_scheduler):
    """
    With a busy interval on one bartender and different current time,
    the scheduler should compute the earliest available slot properly.
    """
    # Mark bartender 0 busy from 5 to 15.
    multi_scheduler.schedulers[0].add_order(5, 10)
    # Bartender 0 can still take an order from time 0 because a 5-minute order (0-5)
    # fits perfectly before the busy interval at 5.
    free_start, bartender_index = multi_scheduler.find_best_free_slot(0, 5)
    # It might return bartender 0 if its free slot is 0 or bartender 1 if that one is chosen.
    assert free_start == 0


def test_add_order_then_free_slot(multi_scheduler):
    """
    After scheduling an order on a specific bartender, the free slot for that bartender
    should update accordingly.
    """
    # Find a free slot from time 0 for a 5-minute order.
    free_start, bartender_index = multi_scheduler.find_best_free_slot(0, 5)
    multi_scheduler.add_order_to_bartender(bartender_index, free_start, 5)

    # For the bartender we just scheduled, the next available time should be free_start + 5.
    updated_free = multi_scheduler.schedulers[bartender_index].find_free_slot(0, 5)
    assert updated_free == free_start + 5


def test_multiple_orders_across_bartenders(multi_scheduler):
    """
    Schedule orders on both bartenders and verify that the scheduler finds the earliest available slot.
    """
    # Mark bartender 0 busy from 0 to 10.
    multi_scheduler.schedulers[0].add_order(0, 10)
    # For a new 5-minute order at time 0, the scheduler should pick bartender 1 as free at 0.
    free_start, bartender_index = multi_scheduler.find_best_free_slot(0, 5)
    assert free_start == 0
    assert bartender_index == 1

    # Now, mark bartender 1 as busy from 0 to 5.
    multi_scheduler.schedulers[1].add_order(0, 5)
    # For another 5-minute order from time 0, check that the earliest free slot across both bartenders is:
    # bartender 0 is busy until 10, and bartender 1 is busy until 5, so the best slot is 5.
    free_start, bartender_index = multi_scheduler.find_best_free_slot(0, 5)
    assert free_start == 5
    # It could choose bartender 1 since its free slot is exactly 5.
    assert bartender_index in [0, 1]
