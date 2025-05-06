from decimal import Decimal

import pytest


# ------------------------------------------------------------------
# GET /restaurants/list/ - Public endpoint to retrieve restaurants
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_get_restaurants_authenticated(api_client, custom_user, restaurant):
    """
    Authenticated request should return a list of restaurants,
    including the one linked to the user.
    """
    api_client.force_authenticate(user=custom_user)
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
def test_get_menu_items_authenticated(api_client, custom_user, restaurant):
    """
    Authenticated request should return available menu items only
    for the specified restaurant.
    """
    api_client.force_authenticate(user=custom_user)

    # Add one available and one unavailable item to the restaurant
    restaurant.items.create(
        restaurant=restaurant,
        name="Latte",
        description="Hot coffee",
        price=Decimal("3.50"),
        category="beverage",
        stock=10,
        available=True,
        item_image_url="http://example.com/latte.png",
    )
    restaurant.items.create(
        restaurant=restaurant,
        name="Mocha",
        description="Chocolate coffee",
        price=Decimal("4.00"),
        category="beverage",
        stock=0,
        available=False,
        item_image_url="http://example.com/mocha.png",
    )

    resp = api_client.get(f"/restaurants/{restaurant.id}/menu/")
    assert resp.status_code == 200, resp.content
    items = resp.json()
    assert isinstance(items, list)
    names = [i["name"] for i in items]
    assert "Latte" in names
    assert "Mocha" not in names

    # check some serialized fields
    item = items[0]
    assert item["item_image_url"] == "http://example.com/latte.png"


@pytest.mark.django_db
def test_get_menu_items_invalid_restaurant_id(api_client, custom_user):
    """
    If the restaurant ID does not exist, the view should return an empty list.
    """
    api_client.force_authenticate(user=custom_user)
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


@pytest.mark.django_db
def test_restaurant_list_invalid_method(api_client, custom_user):
    api_client.force_authenticate(user=custom_user)
    resp = api_client.post("/restaurants/list/", data="{}", content_type="application/json")
    assert resp.status_code == 405


@pytest.mark.django_db
def test_menu_items_invalid_method(api_client, custom_user, restaurant):
    api_client.force_authenticate(user=custom_user)
    resp = api_client.post(f"/restaurants/{restaurant.id}/menu/", data="{}", content_type="application/json")
    assert resp.status_code == 405
