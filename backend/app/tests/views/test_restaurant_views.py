from decimal import Decimal

import pytest

# ------------------------------------------------------------------
# GET /restaurants/list/ - Public endpoint to retrieve restaurants
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_get_restaurants_authenticated(api_client, user, restaurant):
    """
    Authenticated request should return a list of restaurants,
    including the one linked to the user.
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
    Unauthenticated request should return a 401 Unauthorized error.
    """
    response = api_client.get("/restaurants/list/")
    assert response.status_code == 401


# ------------------------------------------------------------------
# GET /restaurants/<id>/menu/ - Returns menu items for a restaurant
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_get_menu_items_authenticated(api_client, user, restaurant):
    """
    Authenticated request should return available menu items only
    for the specified restaurant.
    """
    api_client.force_authenticate(user=user)

    # Add one available and one unavailable item to the restaurant
    restaurant.items.create(
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
    names = [item["name"] for item in data]
    assert "Available Item" in names
    assert "Unavailable Item" not in names


@pytest.mark.django_db
def test_get_menu_items_invalid_restaurant_id(api_client, user):
    """
    If the restaurant ID does not exist, the view should return an empty list.
    """
    api_client.force_authenticate(user=user)
    url = "/restaurants/9999/menu/"
    response = api_client.get(url)
    assert response.status_code == 200, response.content
    assert response.json() == []


@pytest.mark.django_db
def test_get_menu_items_unauthenticated(api_client, restaurant):
    """
    Unauthenticated request should return a 401 Unauthorized error.
    """
    url = f"/restaurants/{restaurant.id}/menu/"
    response = api_client.get(url)
    assert response.status_code == 401
