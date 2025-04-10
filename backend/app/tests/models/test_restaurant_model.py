import time

import pytest


@pytest.mark.django_db
def test_restaurant_str(restaurant):
    """
    The string representation of a Restaurant should return its name.
    """
    assert str(restaurant) == restaurant.name


@pytest.mark.django_db
def test_restaurant_timestamps(restaurant):
    """
    Saving a Restaurant should update the updated_at timestamp while keeping created_at intact.
    """
    assert restaurant.created_at is not None
    assert restaurant.updated_at is not None

    old_updated_at = restaurant.updated_at
    time.sleep(1)
    restaurant.name = "New Name"
    restaurant.save()
    restaurant.refresh_from_db()
    assert restaurant.updated_at > old_updated_at
