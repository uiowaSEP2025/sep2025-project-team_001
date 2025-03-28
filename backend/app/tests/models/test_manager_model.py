import pytest
from django.contrib.auth import get_user_model

from app.models.customer_models import Manager

User = get_user_model()


@pytest.mark.django_db
def test_manager_str():
    """
    Ensure Manager.__str__ returns the expected string.
    """
    user = User.objects.create_user(
        username="manageruser",
        email="manager@example.com",
        password="pass"
    )
    manager_instance = Manager.objects.create(user=user)
    expected_str = f"{user.username} (Manager)"
    assert str(manager_instance) == expected_str
