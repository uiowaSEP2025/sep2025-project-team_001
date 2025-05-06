# app/tests/models/test_custom_user_model.py
import pytest
from app.models.customer_models import CustomUser


@pytest.mark.django_db
def test_create_custom_user(custom_user):
    """
    Using the `custom_user` fixture:
      - username & email set correctly
      - password is hashed & verifies
      - is_active defaults to True
    """
    user = custom_user
    assert user.username == "user1"
    assert user.email == "user1@example.com"

    # Password hashing
    assert user.password != "testpass"
    assert user.check_password("testpass")

    # Defaults
    assert user.is_active is True


@pytest.mark.django_db
def test_name_fields_and_full_name(custom_user):
    """
    Setting first_name/last_name is persisted,
    and get_full_name() returns "First Last".
    """
    user = custom_user
    assert user.get_full_name() == ""  # no names yet

    user.first_name = "First"
    user.last_name = "Last"
    user.save()

    reloaded = CustomUser.objects.get(pk=user.pk)
    assert reloaded.get_full_name() == "First Last"
