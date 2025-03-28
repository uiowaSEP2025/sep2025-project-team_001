import pytest
from django.contrib.auth import get_user_model

from app.models import Customer

# For convenience, retrieve the CustomUser model
User = get_user_model()


@pytest.mark.django_db
def test_create_customer():
    """
    Test that we can create a Customer and it is saved properly.
    """
    # Create a user
    user = User.objects.create_user(
        username="testuser",
        email="test@example.com",
        password="testpass"
    )

    # Create a Customer that references the user
    customer = Customer.objects.create(user=user)

    # Verify relationships
    assert customer.user == user
    assert customer.user.username == "testuser"
    assert customer.user.email == "test@example.com"
    # If you have a 'phone' field on CustomUser, you can set/check it similarly:
    # user.phone = "1234567890"
    # user.save()
    # assert customer.user.phone == "1234567890"


@pytest.mark.django_db
def test_customer_str_representation():
    """
    Test that the __str__ method returns the expected string.
    """
    user = User.objects.create_user(
        username="johndoe",
        email="johndoe@example.com",
        password="testpass"
    )
    customer = Customer.objects.create(user=user)
    assert str(customer) == "johndoe's Customer Profile"


@pytest.mark.django_db
def test_customer_to_dict():
    """
    Test that the to_dict() method returns the correct dictionary.
    """
    user = User.objects.create_user(
        username="janedoe",
        email="janedoe@example.com",
        password="testpass"
    )
    # If your CustomUser model includes a phone field, you can set it here:
    # user.phone = "1234567890"
    # user.save()

    customer = Customer.objects.create(user=user)
    customer_dict = customer.to_dict()

    # Check the contents of the returned dictionary
    assert customer_dict["id"] == customer.id
    assert customer_dict["username"] == "janedoe"
    assert customer_dict["email"] == "janedoe@example.com"
    # assert customer_dict["phone"] == "1234567890"  # if phone field exists
    assert "created_at" in customer_dict
    assert "updated_at" in customer_dict
