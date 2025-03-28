from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model

from app.models.customer_models import Manager, Customer
from app.models.restaurant_models import Restaurant, Item

User = get_user_model()


@pytest.fixture
def manager():
    user = User.objects.create_user(
        username="manager1", email="manager1@example.com", password="pass"
    )
    return Manager.objects.create(user=user)


@pytest.fixture
def customer():
    user = User.objects.create_user(
        username="customer1", email="customer1@example.com", password="pass"
    )
    # Optionally set additional fields (e.g. phone) if needed.
    user.phone = "555-555-5555"
    user.save()
    return Customer.objects.create(user=user)


@pytest.fixture
def restaurant(manager):
    restaurant = Restaurant.objects.create(
        name="Testaurant",
        address="123 Main St",
        phone="555-555-5555",
        restaurant_image="dummy_image_data"
    )
    restaurant.managers.add(manager)
    return restaurant


@pytest.fixture
def item(restaurant):
    return Item.objects.create(
        restaurant=restaurant,
        name="Test Burger",
        description="Delicious burger",
        price=Decimal("9.99"),
        category="Food",
        stock=100,
        available=True,
        base64_image="dummybase64string"
    )
