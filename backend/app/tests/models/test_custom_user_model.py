import pytest
from app.models.customer_models import CustomUser


@pytest.mark.django_db
def test_create_custom_user():
    user = CustomUser.objects.create_user(
        username="testuser",
        email="testuser@example.com",
        password="password123"
    )
    assert user.username == "testuser"
    assert user.email == "testuser@example.com"
    assert user.check_password("password123")
