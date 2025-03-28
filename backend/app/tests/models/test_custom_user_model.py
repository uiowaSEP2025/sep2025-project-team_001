import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_custom_user_creation():
    """
    Ensure that a CustomUser can be created and stores basic fields correctly.
    """
    user = User.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="pass"
    )
    assert user.username == "testuser"
    assert user.email == "testuser@example.com"
