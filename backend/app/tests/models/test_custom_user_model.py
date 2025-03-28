import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_create_custom_user():
    """
    Test that a CustomUser can be created successfully.
    """
    user = User.objects.create_user(
        username="customuser",
        email="custom@example.com",
        password="testpass"
    )

    # Verify the user attributes
    assert user.username == "customuser"
    assert user.email == "custom@example.com"
