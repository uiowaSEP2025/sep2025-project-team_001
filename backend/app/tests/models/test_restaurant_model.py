import time

import pytest
from app.models import CustomUser
from app.models.customer_models import Manager


@pytest.mark.django_db
def test_restaurant_str(restaurant):
    """
    Ensure Restaurant.__str__ returns the restaurant's name.
    """
    assert str(restaurant) == "Testaurant"


@pytest.mark.django_db
def test_restaurant_timestamps(restaurant):
    """
    Verify that created_at and updated_at are automatically set and that updated_at changes on save.
    """
    # Timestamps should be populated upon creation.
    assert restaurant.created_at is not None
    assert restaurant.updated_at is not None

    old_updated_at = restaurant.updated_at
    # Update a field and save to trigger an updated timestamp.
    time.sleep(2)  # Ensure a noticeable time difference
    restaurant.name = "Testaurant Updated"
    restaurant.save()
    assert restaurant.updated_at > old_updated_at


@pytest.mark.django_db
def test_restaurant_managers(restaurant, manager):
    """
    Ensure that the restaurant's managers relationship is set correctly.
    """
    # The restaurant fixture should already have one manager added.
    assert restaurant.managers.count() == 1
    user = CustomUser.objects.create_user(
        username="manager2", email="manager2@example.com", password="pass"
    )
    new_manager = Manager.objects.create(user=user)
    restaurant.managers.add(new_manager)
    assert new_manager in restaurant.managers.all()
