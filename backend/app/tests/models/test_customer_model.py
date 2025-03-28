import pytest
from django.contrib.auth import get_user_model

from app.models.customer_models import Customer

User = get_user_model()


@pytest.mark.django_db
def test_customer_str_and_to_dict():
    """
    Ensure Customer.__str__ returns the expected string and to_dict returns a proper dictionary.
    """
    user = User.objects.create_user(
        username="customeruser",
        email="customer@example.com",
        password="pass"
    )
    # Optionally set a phone number if your CustomUser supports it.
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
