import time

import pytest
from app.models.customer_models import Customer, CustomUser


@pytest.mark.django_db
def test_customer_str_representation():
    user = CustomUser.objects.create_user(username="john", email="john@example.com", password="pass")
    customer = Customer.objects.create(user=user)

    assert str(customer) == "john's Customer Profile"


@pytest.mark.django_db
def test_customer_to_dict():
    user = CustomUser.objects.create_user(
        username="jane", email="jane@example.com", password="pass"
    )
    customer = Customer.objects.create(user=user)

    data = customer.to_dict()
    assert data["id"] == customer.id
    assert data["username"] == "jane"
    assert data["email"] == "jane@example.com"
    assert "created_at" in data
    assert "updated_at" in data


@pytest.mark.django_db
def test_customer_updated_at_changes():
    user = CustomUser.objects.create_user(username="tim", email="tim@example.com", password="pass")
    customer = Customer.objects.create(user=user)

    old_updated_at = customer.updated_at
    time.sleep(1)
    customer.save()
    customer.refresh_from_db()

    assert customer.updated_at > old_updated_at
