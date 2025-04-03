import time

import pytest
from app.models.customer_models import CustomUser, Manager


@pytest.mark.django_db
def test_manager_str():
    """
    Ensure Manager.__str__ returns the expected string.
    """
    user = CustomUser.objects.create_user(
        username="manageruser", email="manager@example.com", password="pass"
    )
    manager_instance = Manager.objects.create(user=user)
    expected_str = f"{user.username} (Manager)"
    assert str(manager_instance) == expected_str


@pytest.mark.django_db
def test_manager_timestamps():
    """
    Verify that the Manager model's created_at and updated_at fields are set correctly.
    """
    user = CustomUser.objects.create_user(
        username="manager_timestamp",
        email="manager_timestamp@example.com",
        password="pass",
    )
    manager_instance = Manager.objects.create(user=user)

    # Check initial timestamps
    assert manager_instance.created_at is not None
    assert manager_instance.updated_at is not None

    old_updated_at = manager_instance.updated_at
    time.sleep(2)  # Ensure a time difference for the update
    # Save again to trigger an update
    manager_instance.save()
    assert manager_instance.updated_at >= old_updated_at
