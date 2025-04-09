from decimal import Decimal

import pytest
from rest_framework.test import APIClient

# --- GET /restaurants/list/ tests ---

@pytest.mark.django_db
def test_get_restaurants_authenticated(api_client, user, restaurant):
    """
    When authenticated, get_restaurants should return a list containing the restaurant.
    """
    api_client.force_authenticate(user=user)
    response = api_client.get("/restaurants/list/")
    assert response.status_code == 200, response.content
    data = response.json()
    assert isinstance(data, list)
    assert any(r["id"] == restaurant.id for r in data)


@pytest.mark.django_db
def test_get_restaurants_unauthenticated(api_client):
    """
    An unauthenticated request to get_restaurants should return a 401 error.
    """
    response = api_client.get("/restaurants/list/")
    assert response.status_code == 401


# --- GET /restaurants/<id>/menu/ tests ---

@pytest.mark.django_db
def test_get_menu_items_authenticated(api_client, user, restaurant):
    """
    When authenticated, get_menu_items should return only available items for the given restaurant.
    """
    api_client.force_authenticate(user=user)

    available_item = restaurant.items.create(
        name="Available Item",
        description="This item is available",
        price=Decimal("9.99"),
        category="Food",
        stock=10,
        available=True,
        base64_image="dummyimage",
    )

    restaurant.items.create(
        name="Unavailable Item",
        description="This item is not available",
        price=Decimal("9.99"),
        category="Food",
        stock=10,
        available=False,
        base64_image="dummyimage",
    )

    url = f"/restaurants/{restaurant.id}/menu/"
    response = api_client.get(url)
    assert response.status_code == 200, response.content
    data = response.json()
    assert isinstance(data, list)
    names = [item["name"] for item in data]
    assert "Available Item" in names
    assert "Unavailable Item" not in names


@pytest.mark.django_db
def test_get_menu_items_invalid_restaurant_id(api_client, user):
    """
    If a restaurant with the given ID does not exist, the view should return an empty list.
    """
    api_client.force_authenticate(user=user)
    url = "/restaurants/9999/menu/"
    response = api_client.get(url)
    assert response.status_code == 200, response.content
    assert response.json() == []


@pytest.mark.django_db
def test_get_menu_items_unauthenticated(api_client, restaurant):
    """
    An unauthenticated request to get_menu_items should return a 401 error.
    """
    url = f"/restaurants/{restaurant.id}/menu/"
    response = api_client.get(url)
    assert response.status_code == 401
