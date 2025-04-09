import json
from decimal import Decimal

import pytest
from app.models.restaurant_models import Item

# --- Fixtures ---

@pytest.fixture
def restaurant_with_user(restaurant):
    from app.models import CustomUser
    user = CustomUser.objects.create_user(username="manageruser", password="pass")
    restaurant.user = user
    restaurant.save()
    return restaurant, user


# --- Tests for menu_items_api ---

@pytest.mark.django_db
def test_menu_items_api_no_restaurant(api_client):
    """
    Unauthenticated request to menu_items_api returns 401.
    """
    response = api_client.get("/api/menu-items/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_menu_items_api_empty_items(api_client, restaurant_with_user):
    """
    When a Restaurant exists but has no items, the view returns an empty items list with 200.
    """
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    restaurant.items.all().delete()

    response = api_client.get("/api/menu-items/")
    assert response.status_code == 200
    data = response.json()
    assert "items" in data
    assert data["items"] == []


@pytest.mark.django_db
def test_menu_items_api_with_items(api_client, restaurant_with_user):
    """
    When a Restaurant exists with items, the view returns a list of items with status 200.
    """
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)

    item1 = Item.objects.create(
        restaurant=restaurant, name="Item1", description="First", price=Decimal("9.99"),
        category="Food", stock=10, available=True, base64_image="img1"
    )
    item2 = Item.objects.create(
        restaurant=restaurant, name="Item2", description="Second", price=Decimal("5.99"),
        category="Drink", stock=20, available=True, base64_image="img2"
    )

    response = api_client.get("/api/menu-items/")
    assert response.status_code == 200
    data = response.json()
    ids = [i["id"] for i in data["items"]]
    assert item1.id in ids
    assert item2.id in ids


@pytest.mark.django_db
def test_menu_items_api_invalid_method(api_client, restaurant_with_user):
    """
    Non-GET methods on menu_items_api should return a 405 error.
    """
    _, user = restaurant_with_user
    api_client.force_authenticate(user=user)

    response = api_client.post("/api/menu-items/", data="{}", content_type="application/json")
    assert response.status_code == 405
    assert "not allowed" in response.json().get("detail", "").lower()


# --- Tests for manage_menu_item ---

@pytest.mark.django_db
def test_manage_menu_item_unauthenticated(api_client):
    """
    Unauthenticated users should receive a 401 when accessing manage_menu_item.
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
    Authenticated user without a restaurant should receive a 403.
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
    assert response.json().get("error") == "Only restaurant accounts can manage menu items."


@pytest.mark.django_db
def test_manage_menu_item_create_missing_fields(api_client, restaurant_with_user):
    """
    Creating an item without a required field (e.g. 'name') should fail with a 400 error.
    """
    _, user = restaurant_with_user
    api_client.force_authenticate(user=user)

    data = {
        "action": "create",
        # Missing "name"
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
    A valid 'create' action successfully creates an item and returns a 201 response.
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
    assert response.json().get("message") == "Item created successfully"
    assert "item" in response.json()


@pytest.mark.django_db
def test_manage_menu_item_update_missing_item_id(api_client, restaurant_with_user):
    """
    An update action without an item_id should return a 400 error.
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
    assert "invalid action or missing item_id" in response.json().get("error", "").lower()


@pytest.mark.django_db
def test_manage_menu_item_update_success(api_client, restaurant_with_user):
    """
    A valid 'update' action updates an existing item and returns a 200 response.
    """
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)

    item = Item.objects.create(
        restaurant=restaurant,
        name="Original",
        description="Original",
        price=Decimal("10.00"),
        category="Food",
        stock=5,
        available=True,
        base64_image="img"
    )

    update_data = {
        "action": "update",
        "item_id": item.id,
        "name": "Updated Item",
        "price": "20.00",
        "category": "Food",
        "stock": "10",
        "image": "newimage",
        "description": "Updated description",
    }

    response = api_client.post("/api/manage-item/", data=json.dumps(update_data), content_type="application/json")
    assert response.status_code == 200
    resp_data = response.json()
    assert resp_data.get("message") == "Item updated successfully"
    item.refresh_from_db()
    assert item.name == "Updated Item"
    assert item.description == "Updated description"
    assert item.base64_image == "newimage"


@pytest.mark.django_db
def test_manage_menu_item_update_with_ingredient_strings(api_client, restaurant_with_user):
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)

    item = Item.objects.create(
        restaurant=restaurant,
        name="With Ingredients",
        price=Decimal("10.00"),
        category="Food",
        stock=5,
        available=True,
        base64_image="img"
    )

    data = {
        "action": "update",
        "item_id": item.id,
        "ingredients": ["Lettuce", "Tomato"],
    }

    response = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 200
    names = list(item.ingredients.values_list("name", flat=True))
    assert set(names) == {"Lettuce", "Tomato"}


@pytest.mark.django_db
def test_manage_menu_item_update_with_ingredient_dicts(api_client, restaurant_with_user):
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)

    item = Item.objects.create(
        restaurant=restaurant,
        name="Dict Ingredients",
        price=Decimal("10.00"),
        category="Food",
        stock=5,
        available=True,
        base64_image="img"
    )

    data = {
        "action": "update",
        "item_id": item.id,
        "ingredients": [{"name": "Bacon"}, {"name": "Cheese"}],
    }

    response = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 200
    names = list(item.ingredients.values_list("name", flat=True))
    assert set(names) == {"Bacon", "Cheese"}


@pytest.mark.django_db
def test_manage_menu_item_update_with_invalid_ingredient_format(api_client, restaurant_with_user):
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)

    item = Item.objects.create(
        restaurant=restaurant,
        name="Bad Ingredients",
        price=Decimal("10.00"),
        category="Food",
        stock=5,
        available=True,
        base64_image="img"
    )

    data = {
        "action": "update",
        "item_id": item.id,
        "ingredients": [{"not_name": "oops"}],
    }

    response = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert "invalid ingredient format" in response.json().get("error", "").lower()


@pytest.mark.django_db
def test_manage_menu_item_delete_success(api_client, restaurant_with_user):
    """
    A valid 'delete' action deletes an existing item and returns a 200 response.
    """
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)

    item = Item.objects.create(
        restaurant=restaurant,
        name="Delete Me",
        description="To delete",
        price=Decimal("12.50"),
        category="Food",
        stock=5,
        available=True,
        base64_image="img"
    )

    data = {"action": "delete", "item_id": item.id}
    response = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 200
    assert response.json().get("message") == "Item deleted successfully"
    with pytest.raises(Item.DoesNotExist):
        Item.objects.get(pk=item.id)


@pytest.mark.django_db
def test_manage_menu_item_invalid_action(api_client, restaurant_with_user):
    """
    An invalid action should return a 400 error indicating an invalid action or missing item_id.
    """
    _, user = restaurant_with_user
    api_client.force_authenticate(user=user)

    data = {"action": "unknown"}
    response = api_client.post("/api/manage-item/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert "invalid action or missing item_id" in response.json().get("error", "").lower()
