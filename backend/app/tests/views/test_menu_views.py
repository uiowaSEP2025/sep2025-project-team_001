import json
from decimal import Decimal

import pytest
from rest_framework.test import APIClient

from app.models.restaurant_models import Restaurant, Item


@pytest.fixture
def api_client(manager):
    client = APIClient()
    client.force_authenticate(user=manager.user)
    return client


# --- Tests for menu_items_api ---

@pytest.mark.django_db
def test_menu_items_api_no_restaurant(api_client, manager):
    """
    When the authenticated manager has no associated Restaurant, the view returns an empty items list with 200.
    """
    # Remove any restaurants associated with this manager.
    Restaurant.objects.filter(managers=manager).delete()
    response = api_client.get("/api/menu-items/")
    # Even if there is no restaurant, the view now returns a 200 with an empty items list.
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["items"] == []


@pytest.mark.django_db
def test_menu_items_api_empty_items(api_client, restaurant):
    """
    When a Restaurant exists but has no items, the view returns an empty items list with 200.
    """
    # Ensure the restaurant has no items.
    restaurant.items.all().delete()
    response = api_client.get("/api/menu-items/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["items"] == []


@pytest.mark.django_db
def test_menu_items_api_with_items(api_client, restaurant):
    """
    When a Restaurant exists with items, the view returns a list of items with status 200.
    """
    # Create two items for the restaurant.
    item1 = Item.objects.create(
        restaurant=restaurant,
        name="Item1",
        description="First item",
        price=Decimal("9.99"),
        category="Food",
        stock=10,
        available=True,
        base64_image="dummy1"
    )
    item2 = Item.objects.create(
        restaurant=restaurant,
        name="Item2",
        description="Second item",
        price=Decimal("5.99"),
        category="Drink",
        stock=20,
        available=True,
        base64_image="dummy2"
    )
    response = api_client.get("/api/menu-items/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    returned_ids = {item["id"] for item in data["items"]}
    assert item1.id in returned_ids
    assert item2.id in returned_ids


@pytest.mark.django_db
def test_menu_items_api_invalid_method(api_client):
    """
    Non-GET methods on menu_items_api should return a 405 error.
    """
    response = api_client.post("/api/menu-items/", data="{}", content_type="application/json")
    assert response.status_code == 405
    data = response.json()
    # DRF returns a default "detail" message instead of an "error" key.
    assert "not allowed" in data.get("detail", "").lower()


# --- Tests for manage_menu_item ---

@pytest.mark.django_db
def test_manage_menu_item_no_restaurant(api_client, manager):
    """
    When the authenticated manager has no associated Restaurant, manage_menu_item returns a 404 error.
    """
    Restaurant.objects.filter(managers=manager).delete()
    data = {
        "action": "create",
        "name": "Test Item",
        "price": "10.00",
        "category": "Food",
        "stock": "5",
        "image": "dummyimage"
    }
    response = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 404
    resp_data = response.json()
    assert resp_data.get("error") in ["Manager or restaurant not found", "Restaurant not found"]


@pytest.mark.django_db
def test_manage_menu_item_create_missing_fields(api_client, restaurant):
    """
    Creating an item without a required field (e.g. 'name') should fail with a 400 error.
    """
    data = {
        "action": "create",
        # "name" is missing
        "price": "10.00",
        "category": "Food",
        "stock": "5",
        "image": "dummyimage"
    }
    response = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    resp_data = response.json()
    error_msg = resp_data.get("error") or resp_data.get("message", "")
    assert "name is required" in error_msg.lower()


@pytest.mark.django_db
def test_manage_menu_item_create_success(api_client, restaurant):
    """
    A valid 'create' action successfully creates an item and returns a 201 response.
    """
    data = {
        "action": "create",
        "name": "Test Item",
        "price": "10.00",
        "category": "Food",
        "stock": "5",
        "image": "dummyimage"
    }
    response = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 201
    resp_data = response.json()
    assert resp_data.get("message") == "Item created successfully"
    assert "item_id" in resp_data
    assert "item_str" in resp_data


@pytest.mark.django_db
def test_manage_menu_item_update_missing_item_id(api_client, restaurant):
    """
    An update action without an item_id should return a 400 error.
    """
    data = {
        "action": "update",
        # Missing item_id
        "name": "Updated Item",
        "price": "12.00",
        "category": "Food",
        "stock": "10",
        "image": "updatedimage"
    }
    response = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    resp_data = response.json()
    assert "invalid action or missing item_id" in resp_data.get("error", "").lower()


@pytest.mark.django_db
def test_manage_menu_item_update_success(api_client, restaurant):
    """
    A valid 'update' action updates an existing item and returns a 200 response.
    """
    # First, create an item.
    create_data = {
        "action": "create",
        "name": "Original Item",
        "price": "15.00",
        "category": "Food",
        "stock": "8",
        "image": "origimage"
    }
    create_response = api_client.post("/api/manage-item/", data=json.dumps(create_data),
                                      content_type="application/json")
    assert create_response.status_code == 201
    create_resp_data = create_response.json()
    item_id = create_resp_data.get("item_id")
    # Update the item.
    update_data = {
        "action": "update",
        "item_id": item_id,
        "name": "Updated Item",
        "price": "20.00",
        "category": "Food",
        "stock": "10",
        "image": "newimage",
        "description": "Updated description"
    }
    update_response = api_client.post("/api/manage-item/", data=json.dumps(update_data),
                                      content_type="application/json")
    assert update_response.status_code == 200
    update_resp_data = update_response.json()
    assert update_resp_data.get("message") == "Item updated successfully"
    # Verify that the item was updated.
    item = Item.objects.get(pk=item_id)
    assert item.name == "Updated Item"
    assert float(item.price) == 20.00
    assert item.base64_image == "newimage"
    assert item.description == "Updated description"


# --- New Tests for manage_menu_item delete and invalid action ---

@pytest.mark.django_db
def test_manage_menu_item_delete_success(api_client, restaurant):
    """
    A valid 'delete' action deletes an existing item and returns a 200 response.
    """
    # Create an item directly.
    item = Item.objects.create(
        restaurant=restaurant,
        name="Delete Me",
        description="Item to be deleted",
        price=Decimal("12.50"),
        category="Food",
        stock=5,
        available=True,
        base64_image="deleteme"
    )
    data = {
        "action": "delete",
        "item_id": item.id
    }
    response = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 200
    resp_data = response.json()
    assert resp_data.get("message") == "Item deleted successfully"
    # Verify that the item no longer exists.
    with pytest.raises(Item.DoesNotExist):
        Item.objects.get(pk=item.id)


@pytest.mark.django_db
def test_manage_menu_item_invalid_action(api_client, restaurant):
    """
    An invalid action should return a 400 error indicating an invalid action or missing item_id.
    """
    data = {
        "action": "unknown"
        # No item_id provided.
    }
    response = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    resp_data = response.json()
    assert "invalid action or missing item_id" in resp_data.get("error", "").lower()
