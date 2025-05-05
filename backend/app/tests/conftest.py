from decimal import Decimal

import pytest
from app.models.customer_models import Customer, CustomUser
from app.models.order_models import Order, OrderItem
from app.models.restaurant_models import Ingredient, Item, Restaurant
from app.models.worker_models import Worker
from rest_framework.test import APIClient


@pytest.fixture
def api_client(db):
    return APIClient()


@pytest.fixture
def custom_user(db):
    """Returns a test CustomUser."""
    return CustomUser.objects.create_user(
        username="user1",
        email="user1@example.com",
        password="testpass",
    )


@pytest.fixture
def customer(db, custom_user):
    """Returns a Customer for the test user."""
    return Customer.objects.create(user=custom_user)


@pytest.fixture
def customer_user(db, custom_user):
    """Returns a (user, customer) tuple for convenience."""
    customer = Customer.objects.create(user=custom_user)
    return custom_user, customer


@pytest.fixture
def restaurant(db, custom_user):
    """Returns a test Restaurant."""
    return Restaurant.objects.create(
        user=custom_user,
        name="Testaurant",
        address="123 Main St",
        phone="555-555-5555",
        restaurant_image_url="http://example.com/test.png"
    )


@pytest.fixture
def restaurant_with_user(db, restaurant):
    """Returns a Restaurant and a new linked CustomUser."""
    linked_user = CustomUser.objects.create_user(
        username="linkeduser",
        email="linked@example.com",
        password="pass"
    )
    restaurant.user = linked_user
    restaurant.save()
    return restaurant, linked_user


@pytest.fixture
def worker(db, restaurant):
    return Worker.objects.create(
        restaurant=restaurant,
        pin="1234",
        role="manager"
    )


@pytest.fixture
def order(db, customer, restaurant):
    return Order.objects.create(customer=customer, restaurant=restaurant)


@pytest.fixture
def burger_item(db, restaurant):
    return Item.objects.create(
        restaurant=restaurant,
        name="Burger",
        description="Delicious beef burger",
        price=Decimal("9.99"),
        category="Food",
        item_image_url="http://example.com/fake.png",
        available=True
    )


@pytest.fixture
def ingredients(db, burger_item):
    pickles = Ingredient.objects.create(item=burger_item, name="Pickles")
    onions = Ingredient.objects.create(item=burger_item, name="Onions")
    return [pickles, onions]


@pytest.fixture
def manager_user_with_worker(db):
    """Returns a dict with user, restaurant, worker, and pin."""
    user = CustomUser.objects.create_user(
        username="manageruser",
        email="manager@example.com",
        password="pass"
    )
    restaurant = Restaurant.objects.create(
        user=user,
        name="Manageraurant",
        address="456 Side St",
        phone="555-123-4567",
        restaurant_image_url="http://example.com/test.png"
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


@pytest.fixture
def manager_client(db, api_client, manager_user_with_worker):
    """Authenticated APIClient for a manager user."""
    api_client.force_authenticate(user=manager_user_with_worker["user"])
    return api_client


@pytest.fixture
def auth_client(db, api_client):
    """Returns an authenticated APIClient using a test user."""
    user = CustomUser.objects.create_user(
        username="stripeuser",
        email="stripe@example.com",
        password="testpass"
    )
    api_client.force_authenticate(user=user)
    return api_client


@pytest.fixture
def order_item(db, order, burger_item):
    """Returns an OrderItem linking order to burger_item."""
    return OrderItem.objects.create(order=order, item=burger_item, quantity=1)


@pytest.fixture
def order_with_item(order_item):
    """Returns an Order with one OrderItem."""
    return order_item.order


@pytest.fixture
def new_item_payload():
    """Returns a sample payload for creating an Item."""
    return {
        "name": "Test Item",
        "description": "Test description",
        "price": "10.00",
        "category": "Food",
        "item_image_url": "http://example.com/test.png",
        "available": True
    }
