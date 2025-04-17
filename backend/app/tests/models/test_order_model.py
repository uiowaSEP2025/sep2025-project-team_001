import json
from datetime import datetime, timedelta
from decimal import Decimal

import pytest
from app.models import CustomUser
from app.models.order_models import Order
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
    api_client.force_authenticate(user=customer.user)
    payload = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [{"item_id": item.pk, "quantity": 2}],
    }
    resp = api_client.post("/order/new/", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 201
    body = resp.json()

    assert body["message"] == "Order created successfully"
    assert "order_id" in body
    # now separate ETAs:
    assert "food_eta_minutes" in body
    assert "beverage_eta_minutes" in body
    assert "estimated_food_ready_time" in body
    assert "estimated_beverage_ready_time" in body


@pytest.mark.django_db
def test_create_order_with_unwanted_ingredients(api_client, customer, restaurant, item):
    ing1 = Ingredient.objects.create(item=item, name="Pickles")
    ing2 = Ingredient.objects.create(item=item, name="Onions")
    api_client.force_authenticate(user=customer.user)

    payload = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [{
            "item_id": item.pk,
            "quantity": 1,
            "unwanted_ingredients": [ing1.pk, ing2.pk],
        }],
    }
    resp = api_client.post("/order/new/", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 201

    order = Order.objects.get(pk=resp.json()["order_id"])
    stored = list(
        order.order_items.first()
        .unwanted_ingredients.values_list("id", flat=True)
    )
    assert sorted(stored) == sorted([ing1.pk, ing2.pk])


@pytest.mark.django_db
def test_create_order_sets_eta_food_only(api_client, customer, restaurant, item):
    # 3 food items -> 15 + 2*3 = 21 -> round to 25
    item.category = "Food"
    item.save()
    api_client.force_authenticate(user=customer.user)

    now = timezone.now().replace(second=0, microsecond=0)
    payload = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [{"item_id": item.pk, "quantity": 3}],
    }
    resp = api_client.post("/order/new/", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 201, resp.json()
    body = resp.json()

    # food ETA is 25, beverage ETA raw 0 → rounded 0
    assert body["food_eta_minutes"] == 25
    assert body["beverage_eta_minutes"] is None

    food_dt = datetime.fromisoformat(body["estimated_food_ready_time"])
    bev_dt = body["estimated_beverage_ready_time"]
    assert food_dt == now + timedelta(minutes=25)
    # when no beverages, estimator still sets now as ready
    assert bev_dt is None


@pytest.mark.django_db
def test_create_order_sets_eta_beverage_only(api_client, customer, restaurant, item):
    # 2 beverages -> beverage ETA = 2 -> rounded 5
    item.category = "beverage"
    item.save()
    api_client.force_authenticate(user=customer.user)

    now = timezone.now().replace(second=0, microsecond=0)
    payload = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [{"item_id": item.pk, "quantity": 2}],
    }
    resp = api_client.post("/order/new/", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 201, resp.json()
    body = resp.json()

    # food ETA still 15 (rounded), beverage ETA 2→5
    assert body["food_eta_minutes"] is None
    assert body["beverage_eta_minutes"] == 5

    food_dt = body["estimated_food_ready_time"]
    bev_dt = datetime.fromisoformat(body["estimated_beverage_ready_time"])
    assert food_dt is None
    assert bev_dt == now + timedelta(minutes=2)


@pytest.mark.django_db
def test_create_order_sets_eta_mixed(api_client, customer, restaurant, burger_item):
    # 1 food (17→20) + 10 bev → 10→10
    burger_item.category = "Food"
    burger_item.save()
    bev = Item.objects.create(
        restaurant=restaurant,
        name="Test Beverage",
        description="",
        price=Decimal("3.50"),
        category="beverage",
        stock=50,
        available=True,
        base64_image="img"
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
    resp = api_client.post("/order/new/", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 201, resp.json()
    body = resp.json()

    # food 17→20, bev 10→10
    assert body["food_eta_minutes"] == 20
    assert body["beverage_eta_minutes"] == 10

    food_dt = datetime.fromisoformat(body["estimated_food_ready_time"])
    bev_dt = datetime.fromisoformat(body["estimated_beverage_ready_time"])
    assert food_dt == now + timedelta(minutes=20)
    assert bev_dt == now + timedelta(minutes=10)


@pytest.mark.django_db
def test_create_order_invalid_data(api_client, customer, restaurant):
    api_client.force_authenticate(user=customer.user)
    payload = {"customer_id": customer.pk, "restaurant_id": restaurant.pk}
    resp = api_client.post("/order/new/", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 400


@pytest.mark.django_db
def test_create_order_invalid_quantity_type(api_client, customer, restaurant, item):
    api_client.force_authenticate(user=customer.user)
    payload = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [{"item_id": item.pk, "quantity": "two"}],
    }
    resp = api_client.post("/order/new/", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 400


@pytest.mark.django_db
def test_create_order_unauthenticated(api_client, customer, restaurant):
    payload = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [],
    }
    resp = api_client.post("/order/new/", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 401


# ------------------------------------------------------------------
# POST /order/estimate/ - Customer requests ETA estimate
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_estimate_order_eta_food_only(api_client, customer, restaurant, item):
    item.category = "Food"
    item.save()
    api_client.force_authenticate(user=customer.user)

    data = {"restaurant_id": restaurant.id, "order_items": [{"item_id": item.id, "quantity": 4}]}
    resp = api_client.post("/order/estimate/", data=json.dumps(data), content_type="application/json")
    assert resp.status_code == 200
    body = resp.json()

    assert "food_eta_minutes" in body
    assert "beverage_eta_minutes" in body
    # food = 15 + 2*4 = 23 → round to 25; no bev → raw 0 → round 0
    assert body["food_eta_minutes"] == 25
    assert body["beverage_eta_minutes"] == 0


@pytest.mark.django_db
def test_estimate_order_eta_beverage_only(api_client, customer, restaurant, item):
    item.category = "beverage"
    item.save()
    api_client.force_authenticate(user=customer.user)

    data = {"restaurant_id": restaurant.id, "order_items": [{"item_id": item.id, "quantity": 3}]}
    resp = api_client.post("/order/estimate/", data=json.dumps(data), content_type="application/json")
    assert resp.status_code == 200
    body = resp.json()

    # food = 15, bev = 3 → round to 5
    assert body["food_eta_minutes"] == 15
    assert body["beverage_eta_minutes"] == 5


@pytest.mark.django_db
def test_estimate_order_eta_mixed(api_client, customer, restaurant, burger_item):
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
            {"item_id": burger_item.id, "quantity": 2},  # food=19→20
            {"item_id": bev.id, "quantity": 5},           # bev=5→5
        ],
    }
    resp = api_client.post("/order/estimate/", data=json.dumps(data), content_type="application/json")
    assert resp.status_code == 200
    body = resp.json()

    # food 19→20, bev 5→5
    assert body["food_eta_minutes"] == 20
    assert body["beverage_eta_minutes"] == 5
