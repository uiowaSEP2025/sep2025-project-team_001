# app/tests/models/test_customer_model.py
import time
from datetime import datetime

import pytest
from app.models.customer_models import Customer
from django.db import IntegrityError


@pytest.mark.django_db
def test_str_representation(customer):
    """
    __str__ should be "<username>'s Customer Profile".
    """
    expected = f"{customer.user.username}'s Customer Profile"
    assert str(customer) == expected


@pytest.mark.django_db
def test_timestamp_auto_now(customer):
    """
    updated_at advances on save.
    """
    before = customer.updated_at
    time.sleep(0.5)
    customer.save()
    customer.refresh_from_db()
    assert customer.updated_at > before


@pytest.mark.django_db
def test_to_dict_defaults(customer):
    """
    to_dict on a fresh customer returns:
      - id as int
      - name == ""
      - username & email from user
      - stripe_customer_id & fcm_token both None
      - created_at/updated_at as datetime
    """
    data = customer.to_dict()
    assert isinstance(data["id"], int)
    assert data["name"] == ""
    assert data["username"] == customer.user.username
    assert data["email"] == customer.user.email
    assert data["stripe_customer_id"] is None
    assert data["fcm_token"] is None
    assert isinstance(data["created_at"], datetime)
    assert isinstance(data["updated_at"], datetime)


@pytest.mark.django_db
def test_to_dict_with_optional_fields(customer):
    """
    Populated stripe_customer_id & fcm_token should appear as set.
    """
    customer.stripe_customer_id = "cus_123"
    customer.fcm_token = "tok_ABC"
    customer.save()

    data = customer.to_dict()
    assert data["stripe_customer_id"] == "cus_123"
    assert data["fcm_token"] == "tok_ABC"


@pytest.mark.django_db
def test_to_dict_name_field(customer, custom_user):
    """
    to_dict() picks up user.first_name.
    """
    custom_user.first_name = "Alice"
    custom_user.save()

    data = customer.to_dict()
    assert data["name"] == "Alice"


@pytest.mark.django_db
def test_blank_fcm_token_roundtrips(customer):
    """
    Explicitly setting fcm_token="" is preserved.
    """
    customer.fcm_token = ""
    customer.save()
    assert customer.to_dict()["fcm_token"] == ""


@pytest.mark.django_db
def test_unicode_name(customer, custom_user):
    """
    Non-ASCII first_name survives round-trip.
    """
    custom_user.first_name = "José 🚀"
    custom_user.save()
    assert customer.to_dict()["name"] == "José 🚀"


@pytest.mark.django_db
def test_unique_user_constraint(customer, custom_user):
    """
    Creating a second Customer for the same CustomUser should error.
    """
    with pytest.raises(IntegrityError):
        Customer.objects.create(user=custom_user)


@pytest.mark.django_db
def test_cascade_delete_user_removes_customer(customer, custom_user):
    """
    Deleting the CustomUser cascades to delete the Customer.
    """
    custom_user.delete()
    assert not Customer.objects.filter(pk=customer.pk).exists()
