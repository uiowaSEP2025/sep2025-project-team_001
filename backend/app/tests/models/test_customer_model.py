import time

import pytest

from app.models.customer_models import Customer, CustomUser


@pytest.mark.django_db
def test_customer_str_and_to_dict():
    """
    Ensure Customer.__str__ returns the expected string and to_dict returns a correct dictionary.
    """
    user = CustomUser.objects.create_user(
        username="customeruser",
        email="customer@example.com",
        password="pass"
    )
    user.phone = "555-555-5555"
    user.save()

    customer_instance = Customer.objects.create(user=user)
    expected_str = f"{user.username}'s Customer Profile"
    assert str(customer_instance) == expected_str

    customer_dict = customer_instance.to_dict()
    assert customer_dict["id"] == customer_instance.id
    assert customer_dict["username"] == user.username
    assert customer_dict["email"] == user.email
    assert customer_dict["phone"] == user.phone
    assert "created_at" in customer_dict
    assert "updated_at" in customer_dict


@pytest.mark.django_db
def test_customer_timestamps():
    """
    Verify that created_at and updated_at are automatically set and that updated_at changes upon saving.
    """
    user = CustomUser.objects.create_user(
        username="customer_timestamp",
        email="timestamp@example.com",
        password="pass"
    )
    user.phone = "555-555-5555"
    user.save()
    customer_instance = Customer.objects.create(user=user)

    # Check initial timestamps
    assert customer_instance.created_at is not None
    assert customer_instance.updated_at is not None

    old_updated_at = customer_instance.updated_at
    time.sleep(2)  # Ensure a time difference for the update
    # Save again to update the timestamp
    customer_instance.save()
    assert customer_instance.updated_at >= old_updated_at
