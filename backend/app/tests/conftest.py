import pytest
from django.contrib.auth import get_user_model
from app.models.customer_models import Manager, Customer
from app.models.restaurant_models import Restaurant
from app.models.restaurant_models import Item

User = get_user_model()

@pytest.fixture
def manager():
    user = User.objects.create_user(
        username="manager1",
        email="manager1@example.com",
        password="pass"
    )
    return Manager.objects.create(user=user)

@pytest.fixture
def customer():
    user = User.objects.create_user(
        username="customer1",
        email="customer1@example.com",
        password="pass"
    )
    return Customer.objects.create(user=user)

@pytest.fixture
def restaurant(manager):
    restaurant = Restaurant.objects.create(
        name="Testaurant",
        address="123 Test St",
        phone="555-1234",
        restaurant_image="dummy_base64_image_data"
    )
    restaurant.managers.add(manager)
    return restaurant

@pytest.fixture
def item(restaurant):
    return Item.objects.create(
        restaurant=restaurant,
        name="Burger",
        description="Delicious burger",
        price="9.99",
        category="Food",
        stock=10,
        available=True,
        base64_image=None
    )
