import json
from decimal import Decimal

import pytest
from app.models.restaurant_models import Item


# ------------------------------------------------------------------
# Stub out image utilities to avoid external calls/padding errors
# ------------------------------------------------------------------
@pytest.fixture(autouse=True)
def patch_image_utils(monkeypatch):
    monkeypatch.setattr(
        "app.views.menu_views.save_image_from_base64",
        lambda b64, folder, ref_id: f"http://test/{folder}/{ref_id}.png",
    )
    monkeypatch.setattr(
        "app.views.menu_views.delete_s3_image",
        lambda url: None,
    )


# ------------------------------------------------------------------
# GET /api/menu-items/ - Retrieve items for a restaurant
# ------------------------------------------------------------------
@pytest.mark.django_db
def test_menu_items_api_no_restaurant(api_client):
    # Unauthenticated -> 401
    response = api_client.get("/api/menu-items/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_menu_items_api_non_restaurant(api_client, custom_user):
    # Authenticated non-restaurant -> 403
    api_client.force_authenticate(user=custom_user)
    resp = api_client.get("/api/menu-items/")
    assert resp.status_code == 403
    assert resp.json()["error"] == "Only restaurant accounts can access this."


@pytest.mark.django_db
def test_menu_items_api_empty_items(api_client, restaurant_with_user):
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    # ensure no items
    restaurant.items.all().delete()
    resp = api_client.get("/api/menu-items/")
    assert resp.status_code == 200
    assert resp.json()["items"] == []


@pytest.mark.django_db
def test_menu_items_api_with_items(api_client, restaurant_with_user):
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    # create two items
    i1 = Item.objects.create(
        restaurant=restaurant, name="One", description="", price=Decimal("1.00"),
        category="Food", stock=1, available=True
    )
    i2 = Item.objects.create(
        restaurant=restaurant, name="Two", description="", price=Decimal("2.00"),
        category="Drink", stock=2, available=True
    )
    resp = api_client.get("/api/menu-items/")
    assert resp.status_code == 200
    ids = [it["id"] for it in resp.json()["items"]]
    assert i1.id in ids and i2.id in ids


@pytest.mark.django_db
def test_menu_items_api_invalid_method(api_client, restaurant_with_user):
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    resp = api_client.post("/api/menu-items/", data="{}", content_type="application/json")
    assert resp.status_code == 405
    assert "not allowed" in resp.json().get("detail", "").lower()


# ------------------------------------------------------------------
# GET /api/statistics/ - Get item stats
# ------------------------------------------------------------------
@pytest.mark.django_db
def test_get_item_statistics_unauthenticated(api_client):
    resp = api_client.get("/api/statistics/")
    assert resp.status_code == 401


@pytest.mark.django_db
def test_get_item_statistics_non_restaurant(api_client, custom_user):
    api_client.force_authenticate(user=custom_user)
    resp = api_client.get("/api/statistics/")
    assert resp.status_code == 403
    assert resp.json()["error"] == "Unauthorized"


@pytest.mark.django_db
def test_get_item_statistics_success(api_client, restaurant_with_user):
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    # create items with times_ordered
    i1 = Item.objects.create(
        restaurant=restaurant, name="A", description="", price=1,
        category="Food", stock=1, available=True
    )
    i2 = Item.objects.create(
        restaurant=restaurant, name="B", description="", price=1,
        category="Food", stock=1, available=True
    )
    i1.times_ordered = 5
    i1.save()
    i2.times_ordered = 10
    i2.save()

    resp = api_client.get("/api/statistics/")
    assert resp.status_code == 200
    data = resp.json()["items"]
    # Should be ordered by descending times_ordered
    assert data[0]["name"] == "B" and data[0]["times_ordered"] == 10
    assert data[1]["name"] == "A" and data[1]["times_ordered"] == 5


# ------------------------------------------------------------------
# POST /api/manage-item/ - Create, update, or delete menu items
# ------------------------------------------------------------------
@pytest.mark.django_db
def test_manage_menu_item_unauthenticated(api_client):
    data = {"action": "create", "name": "X", "price": "1.00", "category": "Food", "stock": "1", "image": "img"}
    resp = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert resp.status_code == 401


@pytest.mark.django_db
def test_manage_menu_item_non_restaurant(api_client, custom_user):
    api_client.force_authenticate(user=custom_user)
    data = {"action": "create", "name": "X", "price": "1.00", "category": "Food", "stock": "1", "image": "img"}
    resp = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert resp.status_code == 403
    assert resp.json()["error"] == "Only restaurant accounts can manage menu items."


@pytest.mark.django_db
def test_manage_menu_item_create_missing_fields(api_client, restaurant_with_user):
    _, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    data = {"action": "create", "price": "1.00", "category": "Food", "stock": "1", "image": "img"}
    resp = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert resp.status_code == 400
    assert "name is required" in resp.json()["error"].lower()


@pytest.mark.django_db
def test_manage_menu_item_create_success(api_client, restaurant_with_user):
    _, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    data = {"action": "create", "name": "X", "price": "1.00", "category": "Food", "stock": "1", "image": "img"}
    resp = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert resp.status_code == 201
    assert resp.json()["message"] == "Item created successfully"
    assert "item" in resp.json()


@pytest.mark.django_db
def test_manage_menu_item_update_missing_item_id(api_client, restaurant_with_user):
    _, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    data = {"action": "update", "name": "Y", "price": "2.00", "category": "Food", "stock": "2", "image": "img"}
    resp = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert resp.status_code == 400
    assert "invalid action or missing item_id" in resp.json()["error"].lower()


@pytest.mark.django_db
def test_manage_menu_item_update_success(api_client, restaurant_with_user):
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    item = Item.objects.create(
        restaurant=restaurant, name="O", description="", price=1,
        category="Food", stock=1, available=True
    )
    data = {
        "action": "update",
        "item_id": item.id,
        "name": "Updated",
        "price": "3.00",
        "category": "Food",
        "stock": "3",
        "image": "img",
        "description": "D"
    }
    resp = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Item updated successfully"


@pytest.mark.django_db
def test_manage_menu_item_invalid_ingredient_format(api_client, restaurant_with_user):
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    item = Item.objects.create(
        restaurant=restaurant, name="I", description="", price=1,
        category="Food", stock=1, available=True
    )
    data = {"action": "update", "item_id": item.id, "ingredients": [123]}
    resp = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert resp.status_code == 400
    assert "invalid ingredient format" in resp.json()["error"].lower()


@pytest.mark.django_db
def test_manage_menu_item_delete_success(api_client, restaurant_with_user):
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    item = Item.objects.create(
        restaurant=restaurant, name="D", description="", price=1,
        category="Food", stock=1, available=True
    )
    data = {"action": "delete", "item_id": item.id}
    resp = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Item deleted successfully"
    with pytest.raises(Item.DoesNotExist):
        Item.objects.get(pk=item.id)


@pytest.mark.django_db
def test_manage_menu_item_invalid_action(api_client, restaurant_with_user):
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    data = {"action": "unknown"}
    resp = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert resp.status_code == 400
    assert "invalid action or missing item_id" in resp.json()["error"].lower()


def test_manage_menu_item_invalid_method(api_client, custom_user):
    # GET on POST-only endpoint => 405
    api_client.force_authenticate(user=custom_user)
    resp = api_client.get("/api/manage-item/")
    assert resp.status_code == 405
