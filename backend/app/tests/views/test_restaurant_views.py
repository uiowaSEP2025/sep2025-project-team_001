from decimal import Decimal

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

from app.models.restaurant_models import Restaurant, Item

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return User.objects.create_user(username="testuser", email="test@example.com", password="pass")


@pytest.fixture
def restaurant():
    return Restaurant.objects.create(
        name="Testaurant",
        address="123 Main St",
        phone="555-555-5555",
        restaurant_image="dummyimage"
    )


@pytest.fixture
def available_item(restaurant):
    return Item.objects.create(
        restaurant=restaurant,
        name="Available Item",
        description="This item is available",
        price=Decimal("9.99"),
        category="Food",
        stock=10,
        available=True,
        base64_image="dummyimage"
    )


@pytest.fixture
def unavailable_item(restaurant):
    return Item.objects.create(
        restaurant=restaurant,
        name="Unavailable Item",
        description="This item is not available",
        price=Decimal("9.99"),
        category="Food",
        stock=10,
        available=False,
        base64_image="dummyimage"
    )


# --- get_restaurants tests ---

@pytest.mark.django_db
def test_get_restaurants_authenticated(api_client, user, restaurant):
    """
    When authenticated, get_restaurants should return a list containing the restaurant.
    """
    api_client.force_authenticate(user=user)
    response = api_client.get("/restaurants/list")
    assert response.status_code == 200, response.content
    data = response.json()
    # Data should be a list and our restaurant should be included.
    assert isinstance(data, list)
    assert any(r["id"] == restaurant.id for r in data)


@pytest.mark.django_db
def test_get_restaurants_unauthenticated(api_client):
    """
    An unauthenticated request to get_restaurants should return a 401 error.
    """
    response = api_client.get("/restaurants/list")
    assert response.status_code == 401


# --- get_menu_items tests ---

@pytest.mark.django_db
def test_get_menu_items_authenticated(api_client, user, restaurant, available_item, unavailable_item):
    """
    When authenticated, get_menu_items should return only available items for the given restaurant name.
    """
    api_client.force_authenticate(user=user)
    # URL uses restaurant name as a parameter.
    url = f"/restaurants/{restaurant.name}/menu/"
    response = api_client.get(url)
    assert response.status_code == 200, response.content
    data = response.json()
    # Expect a list of items.
    assert isinstance(data, list)
    # Only available_item should be returned.
    returned_names = [item["name"] for item in data]
    assert available_item.name in returned_names
    assert unavailable_item.name not in returned_names


@pytest.mark.django_db
def test_get_menu_items_invalid_restaurant(api_client, user):
    """
    When a restaurant with the given name does not exist, get_menu_items should return an empty list.
    """
    api_client.force_authenticate(user=user)
    url = "/restaurants/Nonexistent/menu/"
    response = api_client.get(url)
    assert response.status_code == 200, response.content
    data = response.json()
    assert data == []


@pytest.mark.django_db
def test_get_menu_items_unauthenticated(api_client, restaurant):
    """
    An unauthenticated request to get_menu_items should return a 401 error.
    """
    url = f"/restaurants/{restaurant.name}/menu/"
    response = api_client.get(url)
    assert response.status_code == 401
