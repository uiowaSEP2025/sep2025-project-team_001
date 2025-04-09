import pytest
from decimal import Decimal
from app.models.customer_models import CustomUser, Customer
from app.models.restaurant_models import Restaurant, Item
from app.models.worker_models import Worker


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
