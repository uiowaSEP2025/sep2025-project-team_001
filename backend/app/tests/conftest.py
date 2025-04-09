from decimal import Decimal

import pytest
from app.models import Order
from app.models.customer_models import Customer, CustomUser
from app.models.restaurant_models import Ingredient, Item, Restaurant
from app.models.worker_models import Worker
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return CustomUser.objects.create_user(
        username="user1",
        email="user1@example.com",
        password="testpass",
    )


@pytest.fixture
def customer(user):
    return Customer.objects.create(user=user)


@pytest.fixture
def restaurant(user):
    return Restaurant.objects.create(
        user=user,
        name="Testaurant",
        address="123 Main St",
        phone="555-555-5555",
        restaurant_image="image-data"
    )


@pytest.fixture
def restaurant_with_user(restaurant):
    custom_user = CustomUser.objects.create_user(
        username="linkeduser", email="linked@example.com", password="pass"
    )
    restaurant.user = custom_user
    restaurant.save()
    return restaurant, custom_user


@pytest.fixture
def worker(restaurant):
    return Worker.objects.create(
        restaurant=restaurant,
        pin="1234",
        role="manager"
    )


@pytest.fixture
def item(restaurant):
    return Item.objects.create(
        restaurant=restaurant,
        name="Test Burger",
        description="A tasty burger",
        price=Decimal("8.99"),
        category="Food",
        stock=20,
        available=True,
        base64_image="base64-encoded-image"
    )


@pytest.fixture
def order(customer, restaurant):
    return Order.objects.create(customer=customer, restaurant=restaurant)


@pytest.fixture
def burger_item(restaurant):
    return Item.objects.create(
        restaurant=restaurant,
        name="Burger",
        description="Delicious beef burger",
        price=Decimal("9.99"),
        category="Food",
        stock=10,
        available=True,
        base64_image="fake-image"
    )


@pytest.fixture
def ingredients(burger_item):
    pickles = Ingredient.objects.create(item=burger_item, name="Pickles")
    onions = Ingredient.objects.create(item=burger_item, name="Onions")
    return [pickles, onions]


@pytest.fixture
def manager_user_with_worker():
    """
    Returns a dict: {
        user: CustomUser,
        restaurant: Restaurant,
        worker: Worker,
        pin: str
    }
    """
    user = CustomUser.objects.create_user(
        username="manageruser",
        email="manager@example.com",
        password="securepass"
    )
    restaurant = Restaurant.objects.create(
        user=user,
        name="PinTestaurant",
        address="123 Pin St",
        phone="999-888-7777",
        restaurant_image="restaurant-img"
    )
    worker = Worker.objects.create(
        restaurant=restaurant,
        pin="7777",
        role="manager"
    )
    return {
        "user": user,
        "restaurant": restaurant,
        "worker": worker,
        "pin": "7777"
    }
