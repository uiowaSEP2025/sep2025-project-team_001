import json
from datetime import datetime, timedelta
from decimal import Decimal

import pytest
from app.models import CustomUser
from app.models.order_models import Order, OrderItem
from app.models.restaurant_models import Ingredient, Item
from django.utils import timezone
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def restaurant_with_user(restaurant):
    user = CustomUser.objects.create_user(
        username="mgruser", email="mgr@example.com", password="pass"
    )
    restaurant.user = user
    restaurant.save()
    return restaurant, user


# ------------------------------------------------------------------
# POST /order/new/ - Create a new order
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_create_order_success(api_client, customer, restaurant, item):
    """
    Creates an order with one item. Should return 201 and success message,
    and include order_id, eta_minutes, and both ETA timestamps in the JSON.
    """
    api_client.force_authenticate(user=customer.user)
    payload = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [{"item_id": item.pk, "quantity": 2}],
    }
    resp = api_client.post(
        "/order/new/", data=json.dumps(payload), content_type="application/json"
    )
    assert resp.status_code == 201
    body = resp.json()
    assert body["message"] == "Order created successfully"
    assert "order_id" in body
    assert "food_eta_minutes" in body
    assert "beverage_eta_minutes" in body
    assert "estimated_food_ready_time" in body
    assert "estimated_beverage_ready_time" in body


@pytest.mark.django_db
def test_create_order_with_unwanted_ingredients(api_client, customer, restaurant, item):
    """
    Creates an order and stores unwanted ingredients in the order item;
    ETA behavior is unchanged here.
    """
    ing1 = Ingredient.objects.create(item=item, name="Pickles")
    ing2 = Ingredient.objects.create(item=item, name="Onions")
    api_client.force_authenticate(user=customer.user)

    payload = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [
            {
                "item_id": item.pk,
                "quantity": 1,
                "unwanted_ingredients": [ing1.pk, ing2.pk],
            }
        ],
    }
    resp = api_client.post(
        "/order/new/", data=json.dumps(payload), content_type="application/json"
    )
    assert resp.status_code == 201
    order = Order.objects.get(pk=resp.json()["order_id"])
    stored = list(
        order.order_items.first()
        .unwanted_ingredients.values_list("id", flat=True)
    )
    assert sorted(stored) == sorted([ing1.pk, ing2.pk])


@pytest.mark.django_db
def test_create_order_sets_eta_food_only(api_client, customer, restaurant, item):
    """
    3 food items -> 15 + 2*3 = 21 -> round to 25.
    Should get eta_minutes=25, food_ready=now+25, beverage_ready=now.
    """
    item.category = "Food"
    item.save()
    api_client.force_authenticate(user=customer.user)

    now = timezone.now().replace(second=0, microsecond=0)
    payload = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [{"item_id": item.pk, "quantity": 3}],
    }
    resp = api_client.post(
        "/order/new/", data=json.dumps(payload), content_type="application/json"
    )
    assert resp.status_code == 201, resp.json()
    body = resp.json()

    assert body["food_eta_minutes"] == 25
    assert body["beverage_eta_minutes"] is None

    # Parse timestamps
    food_dt = datetime.fromisoformat(body["estimated_food_ready_time"])
    bev_dt = body["estimated_beverage_ready_time"]
    assert food_dt == now + timedelta(minutes=25)
    assert bev_dt is None


@pytest.mark.django_db
def test_create_order_sets_eta_beverage_only(api_client, customer, restaurant, item):
    """
    2 beverages -> bev ETA=2, food ETA=15 -> overall=15.
    """
    item.category = "beverage"
    item.save()
    api_client.force_authenticate(user=customer.user)

    now = timezone.now().replace(second=0, microsecond=0)
    payload = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [{"item_id": item.pk, "quantity": 2}],
    }
    resp = api_client.post(
        "/order/new/", data=json.dumps(payload), content_type="application/json"
    )
    assert resp.status_code == 201, resp.json()
    body = resp.json()

    assert body["food_eta_minutes"] is None
    assert body["beverage_eta_minutes"] == 5
    food_dt = body["estimated_food_ready_time"]
    bev_dt = datetime.fromisoformat(body["estimated_beverage_ready_time"])
    assert food_dt is None
    assert bev_dt == now + timedelta(minutes=2)


@pytest.mark.django_db
def test_create_order_sets_eta_mixed(api_client, customer, restaurant, burger_item):
    """
    Mixed: 1 food (17->20) + 10 bev (10) -> overall=20.
    """
    burger_item.category = "Food"
    burger_item.save()
    bev = Item.objects.create(
        restaurant=restaurant,
        name="Soda",
        description="",
        price=Decimal("1.00"),
        category="beverage",
        stock=10,
        available=True,
        base64_image="",
    )

    api_client.force_authenticate(user=customer.user)
    now = timezone.now().replace(second=0, microsecond=0)
    payload = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [
            {"item_id": burger_item.pk, "quantity": 1},
            {"item_id": bev.pk, "quantity": 10},
        ],
    }
    resp = api_client.post(
        "/order/new/", data=json.dumps(payload), content_type="application/json"
    )
    assert resp.status_code == 201, resp.json()
    body = resp.json()

    assert body["food_eta_minutes"] == 20
    assert body["beverage_eta_minutes"] == 10
    food_dt = datetime.fromisoformat(body["estimated_food_ready_time"])
    bev_dt = datetime.fromisoformat(body["estimated_beverage_ready_time"])
    assert food_dt == now + timedelta(minutes=20)
    assert bev_dt == now + timedelta(minutes=10)


@pytest.mark.django_db
def test_create_order_invalid_data(api_client, customer, restaurant):
    """
    Omitting order_items should 400.
    """
    api_client.force_authenticate(user=customer.user)
    payload = {"customer_id": customer.pk, "restaurant_id": restaurant.pk}
    resp = api_client.post(
        "/order/new/", data=json.dumps(payload), content_type="application/json"
    )
    assert resp.status_code == 400


@pytest.mark.django_db
def test_create_order_invalid_quantity_type(api_client, customer, restaurant, item):
    """
    Passing quantity as string should 400.
    """
    api_client.force_authenticate(user=customer.user)
    payload = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [{"item_id": item.pk, "quantity": "two"}],
    }
    resp = api_client.post(
        "/order/new/", data=json.dumps(payload), content_type="application/json"
    )
    assert resp.status_code == 400


@pytest.mark.django_db
def test_create_order_unauthenticated(api_client, customer, restaurant):
    """
    Unauthenticated user -> 401.
    """
    payload = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [],
    }
    resp = api_client.post(
        "/order/new/", data=json.dumps(payload), content_type="application/json"
    )
    assert resp.status_code == 401


# ------------------------------------------------------------------
# GET /retrieve/orders/ - Manager views active orders
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_retrieve_active_orders_success(api_client, restaurant_with_user, customer, item):
    """
    Manager should receive active orders.
    """
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)

    order = Order.objects.create(
        customer=customer, restaurant=restaurant, status="pending", total_price=0
    )
    OrderItem.objects.create(order=order, item=item, quantity=1)

    resp = api_client.get("/retrieve/orders/")
    assert resp.status_code == 200
    data = resp.json()
    assert any(o["id"] == order.id for o in data)


@pytest.mark.django_db
def test_retrieve_active_orders_none_exist(api_client, restaurant_with_user):
    """
    No orders -> [].
    """
    _, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    resp = api_client.get("/retrieve/orders/")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.django_db
def test_retrieve_active_orders_unauthorized(api_client):
    """
    Non-restaurant user -> 403.
    """
    user = CustomUser.objects.create_user(
        username="unauth", email="unauth@example.com", password="pass"
    )
    api_client.force_authenticate(user=user)
    resp = api_client.get("/retrieve/orders/")
    assert resp.status_code == 403


# ------------------------------------------------------------------
# PATCH /orders/<restaurant_id>/<order_id>/completed/ - Mark completed
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_mark_order_completed_success(api_client, restaurant_with_user, customer, item):
    """
    PATCH /orders/<rest_id>/<order_id>/completed/
    """
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)

    order = Order.objects.create(
        customer=customer, restaurant=restaurant, status="pending", total_price=0
    )
    resp = api_client.patch(
        f"/orders/{restaurant.pk}/{order.id}/completed/", data={}, format="json"
    )
    assert resp.status_code == 200
    order.refresh_from_db()
    assert order.status == "completed"


@pytest.mark.django_db
def test_mark_order_completed_not_found(api_client, restaurant_with_user):
    """
    Non-existent order -> 404.
    """
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    resp = api_client.patch(
        f"/orders/{restaurant.pk}/9999/completed/", data={}, format="json"
    )
    assert resp.status_code == 404


# ------------------------------------------------------------------
# GET /order/customer/ - Customer views own orders
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_get_customer_orders_success(api_client, customer, restaurant, item):
    api_client.force_authenticate(user=customer.user)
    order = Order.objects.create(
        customer=customer, restaurant=restaurant, status="pending", total_price=0
    )
    OrderItem.objects.create(order=order, item=item, quantity=1)
    resp = api_client.get("/order/customer/")
    assert resp.status_code == 200
    assert any(o["id"] == order.id for o in resp.json())


@pytest.mark.django_db
def test_get_customer_orders_none_exist(api_client, customer):
    api_client.force_authenticate(user=customer.user)
    resp = api_client.get("/order/customer/")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.django_db
def test_get_customer_orders_not_customer(api_client):
    user = CustomUser.objects.create_user(
        username="notcust", email="x@example.com", password="pass"
    )
    api_client.force_authenticate(user=user)
    resp = api_client.get("/order/customer/")
    assert resp.status_code == 404


# ------------------------------------------------------------------
# POST /order/estimate/ - Customer requests ETA estimate
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_estimate_order_eta_food_only(api_client, customer, restaurant, item):
    """
    Food only: 4 items→23→25.
    """
    item.category = "Food"
    item.save()
    api_client.force_authenticate(user=customer.user)
    data = {"restaurant_id": restaurant.id, "order_items": [{"item_id": item.id, "quantity": 4}]}
    resp = api_client.post("/order/estimate/", data=json.dumps(data), content_type="application/json")
    assert resp.status_code == 200
    body = resp.json()
    # food ETA = 15 + 2*4 = 23 → round to 25; no beverages → bev=0
    assert "food_eta_minutes" in body
    assert "beverage_eta_minutes" in body
    assert body["food_eta_minutes"] == 25
    assert body["beverage_eta_minutes"] == 0


@pytest.mark.django_db
def test_estimate_order_eta_beverage_only(api_client, customer, restaurant, item):
    """
    Bev only: 3→3, food=15→ overall=15.
    """
    item.category = "beverage"
    item.save()
    api_client.force_authenticate(user=customer.user)
    data = {"restaurant_id": restaurant.id, "order_items": [{"item_id": item.id, "quantity": 3}]}
    resp = api_client.post("/order/estimate/", data=json.dumps(data), content_type="application/json")
    assert resp.status_code == 200
    body = resp.json()
    # num_food=0 → food=15; num_bev=3 → raw_bev=3→round5
    assert "food_eta_minutes" in body
    assert "beverage_eta_minutes" in body
    assert body["food_eta_minutes"] == 15
    assert body["beverage_eta_minutes"] == 5


@pytest.mark.django_db
def test_estimate_order_eta_mixed(api_client, customer, restaurant, burger_item):
    """
    Mixed: food=2→19→20, bev=10→10
    """
    burger_item.category = "Food"
    burger_item.save()
    bev = Item.objects.create(
        restaurant=restaurant, name="Soda", description="", price=1,
        category="beverage", stock=10, available=True
    )
    api_client.force_authenticate(user=customer.user)
    data = {
        "restaurant_id": restaurant.id,
        "order_items": [
            {"item_id": burger_item.id, "quantity": 2},
            {"item_id": bev.id, "quantity": 10},
        ],
    }
    resp = api_client.post("/order/estimate/", data=json.dumps(data), content_type="application/json")
    assert resp.status_code == 200
    body = resp.json()
    # food: 15+2*1=17→round 20; bev:10→round 10
    assert "food_eta_minutes" in body
    assert "beverage_eta_minutes" in body
    assert body["food_eta_minutes"] == 20
    assert body["beverage_eta_minutes"] == 10
