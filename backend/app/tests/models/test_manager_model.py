import pytest
from django.contrib.auth import get_user_model

from app.models import Manager

User = get_user_model()


@pytest.mark.django_db
def test_create_manager():
    """
    Test that a Manager can be created and linked to a CustomUser.
    """
    # Create a CustomUser
    user = User.objects.create_user(
        username="manageruser",
        email="manager@example.com",
        password="testpass"
    )

    # Create a Manager associated with the user
    manager = Manager.objects.create(user=user)

    # Assert the relationship and that timestamps are set
    assert manager.user == user
    assert manager.created_at is not None
    assert manager.updated_at is not None


@pytest.mark.django_db
def test_manager_str_representation():
    """
    Test that the __str__ method returns the expected string.
    """
    user = User.objects.create_user(
        username="manageruser",
        email="manager@example.com",
        password="testpass"
    )
    manager = Manager.objects.create(user=user)

    # Expected string: "<username> (Manager)"
    expected_str = f"{user.username} (Manager)"
    assert str(manager) == expected_str
