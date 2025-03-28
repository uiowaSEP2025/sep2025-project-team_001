import json
from decimal import Decimal

import pytest

from app.models.restaurant_models import Restaurant, Item


# --- Tests for menu_items_api ---

@pytest.mark.django_db
def test_menu_items_api_no_restaurant(client):
    """
    If no Restaurant exists, menu_items_api should return a 404 error.
    """
    # Remove any existing restaurants.
    Restaurant.objects.all().delete()
    response = client.get("/api/menu-items/")
    assert response.status_code == 404
    data = json.loads(response.content)
    assert data.get("error") == "Restaurant not found"


@pytest.mark.django_db
def test_menu_items_api_empty_items(client, restaurant):
    """
    When a Restaurant exists but has no items, an empty items list should be returned.
    """
    # Ensure the restaurant has no items.
    restaurant.items.all().delete()
    response = client.get("/api/menu-items/")
    assert response.status_code == 200
    data = json.loads(response.content)
    assert "items" in data
    assert data["items"] == []


@pytest.mark.django_db
def test_menu_items_api_with_items(client, restaurant):
    """
    When a Restaurant exists with items, the view should return a list of items.
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
    response = client.get("/api/menu-items/")
    assert response.status_code == 200
    data = json.loads(response.content)
    assert "items" in data
    returned_ids = {item["id"] for item in data["items"]}
    assert item1.id in returned_ids
    assert item2.id in returned_ids


@pytest.mark.django_db
def test_menu_items_api_invalid_method(client):
    """
    Non-GET methods on menu_items_api should return a 405 error.
    """
    response = client.post("/api/menu-items/", data="{}", content_type="application/json")
    assert response.status_code == 405
    data = json.loads(response.content)
    assert data.get("error") == "Method not allowed"


# --- Tests for manage_menu_item ---

@pytest.mark.django_db
def test_manage_menu_item_no_restaurant(client):
    """
    If no Restaurant exists, manage_menu_item should return a 404 error.
    """
    Restaurant.objects.all().delete()
    data = {
        "action": "create",
        "name": "Test Item",
        "price": "10.00",
        "category": "Food",
        "stock": "5",
        "image": "dummyimage"
    }
    response = client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 404
    resp_data = json.loads(response.content)
    assert resp_data.get("error") == "Restaurant not found"


@pytest.mark.django_db
def test_manage_menu_item_create_missing_fields(client, restaurant):
    """
    Attempting to create an item without required fields (e.g. name) should fail.
    """
    data = {
        "action": "create",
        # Missing "name"
        "price": "10.00",
        "category": "Food",
        "stock": "5",
        "image": "dummyimage"
    }
    response = client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    resp_data = json.loads(response.content)
    # The view returns an error message that capitalizes and replaces underscores;
    # we check that the error message mentions "Name" is required.
    assert "name is required" in resp_data.get("message", resp_data.get("error", ""))


@pytest.mark.django_db
def test_manage_menu_item_create_success(client, restaurant):
    """
    Test that a valid 'create' action successfully creates an item.
    """
    data = {
        "action": "create",
        "name": "Test Item",
        "price": "10.00",
        "category": "Food",
        "stock": "5",
        "image": "dummyimage"
    }
    response = client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 201
    resp_data = json.loads(response.content)
    assert resp_data.get("message") == "Item created successfully"
    assert "item_id" in resp_data
    assert "item_str" in resp_data


@pytest.mark.django_db
def test_manage_menu_item_update_missing_item_id(client, restaurant):
    """
    An update action without an item_id should return an error.
    """
    data = {
        "action": "update",
        # No item_id provided.
        "name": "Updated Item",
        "price": "12.00",
        "category": "Food",
        "stock": "10",
        "image": "updatedimage"
    }
    response = client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    resp_data = json.loads(response.content)
    assert "Invalid action or missing item_id" in resp_data.get("error", "")


@pytest.mark.django_db
def test_manage_menu_item_update_success(client, restaurant):
    """
    Test that a valid 'update' action updates an existing item.
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
    create_response = client.post("/api/manage-item/", data=json.dumps(create_data), content_type="application/json")
    assert create_response.status_code == 201
    create_resp_data = json.loads(create_response.content)
    item_id = create_resp_data.get("item_id")
    # Now, update the item.
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
    update_response = client.post("/api/manage-item/", data=json.dumps(update_data), content_type="application/json")
    assert update_response.status_code == 200
    update_resp_data = json.loads(update_response.content)
    assert update_resp_data.get("message") == "Item updated successfully"
    # Verify that the item was updated.
    from app.models.restaurant_models import Item
    item = Item.objects.get(pk=item_id)
    assert item.name == "Updated Item"
    assert float(item.price) == 20.00
    assert item.base64_image == "newimage"
    assert item.description == "Updated description"


@pytest.mark.django_db
def test_manage_menu_item_delete_missing_item_id(client, restaurant):
    """
    A delete action without providing an item_id should fail.
    """
    data = {
        "action": "delete"
        # item_id missing
    }
