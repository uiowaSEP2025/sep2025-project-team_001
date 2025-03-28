import pytest

from app.models.customer_models import CustomUser


@pytest.mark.django_db
def test_custom_user_creation():
    """
    Ensure that a CustomUser can be created and stores basic fields correctly.
    """
    user = CustomUser.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="pass"
    )
    assert user.username == "testuser"
    assert user.email == "testuser@example.com"
