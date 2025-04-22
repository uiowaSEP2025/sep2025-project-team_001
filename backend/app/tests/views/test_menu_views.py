import json
from decimal import Decimal

import pytest
from app.models.restaurant_models import Item


# ------------------------------------------------------------------
# GET /api/menu-items/ - Retrieve items for a restaurant
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_menu_items_api_no_restaurant(api_client):
    """
    Unauthenticated user should receive 401 when accessing the menu-items endpoint.
    """
    response = api_client.get("/api/menu-items/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_menu_items_api_empty_items(api_client, restaurant_with_user):
    """
    Authenticated request should return an empty items list if the restaurant has no items.
    """
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    restaurant.items.all().delete()

    response = api_client.get("/api/menu-items/")
    assert response.status_code == 200
    assert response.json()["items"] == []


@pytest.mark.django_db
def test_menu_items_api_with_items(api_client, restaurant_with_user):
    """
    Authenticated request should return all available items for the restaurant.
    """
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)

    item1 = Item.objects.create(
        restaurant=restaurant, name="Item1", description="First",
        price=Decimal("9.99"), category="Food", stock=10,
        available=True, base64_image="img1"
    )
    item2 = Item.objects.create(
        restaurant=restaurant, name="Item2", description="Second",
        price=Decimal("5.99"), category="Drink", stock=20,
        available=True, base64_image="img2"
    )

    response = api_client.get("/api/menu-items/")
    assert response.status_code == 200
    ids = [i["id"] for i in response.json()["items"]]
    assert item1.id in ids
    assert item2.id in ids


@pytest.mark.django_db
def test_menu_items_api_invalid_method(api_client, restaurant_with_user):
    """
    Non-GET methods on menu-items endpoint should return 405 Method Not Allowed.
    """
    _, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    response = api_client.post("/api/menu-items/", data="{}", content_type="application/json")
    assert response.status_code == 405
    assert "not allowed" in response.json().get("detail", "").lower()


# ------------------------------------------------------------------
# POST /api/manage-item/ - Create, update, or delete menu items
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_manage_menu_item_unauthenticated(api_client):
    """
    Unauthenticated request to manage-item endpoint should return 401.
    """
    data = {
        "action": "create",
        "name": "Test Item",
        "price": "10.00",
        "category": "Food",
        "stock": "5",
        "image": "dummyimage",
    }
    response = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 401


@pytest.mark.django_db
def test_manage_menu_item_authenticated_but_no_restaurant(api_client, user):
    """
    Authenticated user without a restaurant should receive 403.
    """
    api_client.force_authenticate(user=user)
    data = {
        "action": "create",
        "name": "Test Item",
        "price": "10.00",
        "category": "Food",
        "stock": "5",
        "image": "dummyimage",
    }
    response = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 403
    assert response.json()["error"] == "Only restaurant accounts can manage menu items."


@pytest.mark.django_db
def test_manage_menu_item_create_missing_fields(api_client, restaurant_with_user):
    """
    Creating an item without required fields should return 400.
    """
    _, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    data = {
        "action": "create",
        "price": "10.00",
        "category": "Food",
        "stock": "5",
        "image": "dummyimage",
    }
    response = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert "name is required" in response.json().get("error", "").lower()


@pytest.mark.django_db
def test_manage_menu_item_create_success(api_client, restaurant_with_user):
    """
    Creating an item with valid data should return 201 and create the item.
    """
    _, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    data = {
        "action": "create",
        "name": "Test Item",
        "price": "10.00",
        "category": "Food",
        "stock": "5",
        "image": "dummyimage",
    }
    response = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 201
    assert response.json()["message"] == "Item created successfully"
    assert "item" in response.json()


@pytest.mark.django_db
def test_manage_menu_item_update_missing_item_id(api_client, restaurant_with_user):
    """
    Updating an item without specifying item_id should return 400.
    """
    _, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    data = {
        "action": "update",
        "name": "Updated Item",
        "price": "12.00",
        "category": "Food",
        "stock": "10",
        "image": "updatedimage",
    }
    response = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert "invalid action or missing item_id" in response.json()["error"].lower()


@pytest.mark.django_db
def test_manage_menu_item_update_success(api_client, restaurant_with_user):
    """
    Updating an existing item should modify its fields and return 200.
    """
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    item = Item.objects.create(
        restaurant=restaurant, name="Original", price=Decimal("10.00"),
        category="Food", stock=5, available=True, base64_image="img"
    )
    data = {
        "action": "update",
        "item_id": item.id,
        "name": "Updated Item",
        "price": "20.00",
        "category": "Food",
        "stock": "10",
        "image": "newimage",
        "description": "Updated description",
    }
    response = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 200
    assert response.json()["message"] == "Item updated successfully"


@pytest.mark.django_db
def test_manage_menu_item_delete_success(api_client, restaurant_with_user):
    """
    Deleting an existing item should remove it and return 200.
    """
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    item = Item.objects.create(
        restaurant=restaurant, name="Delete Me", description="To delete",
        price=Decimal("12.50"), category="Food", stock=5,
        available=True, base64_image="img"
    )
    data = {"action": "delete", "item_id": item.id}
    response = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 200
    assert response.json()["message"] == "Item deleted successfully"
    with pytest.raises(Item.DoesNotExist):
        Item.objects.get(pk=item.id)


@pytest.mark.django_db
def test_manage_menu_item_invalid_action(api_client, restaurant_with_user):
    """
    An unrecognized action should return 400 with an error message.
    """
    _, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    data = {"action": "unknown"}
    response = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert "invalid action or missing item_id" in response.json()["error"].lower()
