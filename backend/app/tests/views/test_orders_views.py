import json
from datetime import datetime, timedelta
from decimal import Decimal

import pytest
from app.models import Worker
from app.models.customer_models import CustomUser
from app.models.order_models import Order, OrderItem
from app.models.restaurant_models import Item
from django.utils import timezone
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture(autouse=True)
def patch_fcm(monkeypatch):
    # Stub out FCM notifications
    monkeypatch.setattr(
        "app.views.orders_views.send_fcm_httpv1",
        lambda *args, **kwargs: None
    )
    monkeypatch.setattr(
        "app.views.orders_views.send_notification_to_device",
        lambda *args, **kwargs: None
    )


# ------------------------------------------------------------------
# POST /order/new/ - Create a new order
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_create_order_success(api_client, customer, restaurant, burger_item):
    api_client.force_authenticate(user=customer.user)
    payload = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [{"item_id": burger_item.pk, "quantity": 2}],
    }
    resp = api_client.post(
        "/order/new/",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert resp.status_code == 201
    data = resp.json()
    assert data["message"] == "Order created successfully"
    assert isinstance(data["order_id"], int)
    # All ETA fields should be present (can be null)
    assert set(data.keys()) >= {
        "food_eta_minutes",
        "beverage_eta_minutes",
        "estimated_food_ready_time",
        "estimated_beverage_ready_time",
    }


@pytest.mark.django_db
def test_create_order_with_unwanted_ingredients(api_client, customer, restaurant, burger_item, ingredients):
    api_client.force_authenticate(user=customer.user)
    ing_ids = [ing.pk for ing in ingredients]
    payload = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [{
            "item_id": burger_item.pk,
            "quantity": 1,
            "unwanted_ingredients": ing_ids,
        }],
    }
    resp = api_client.post(
        "/order/new/",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert resp.status_code == 201
    order = Order.objects.get(pk=resp.json()["order_id"])
    stored = list(
        order.order_items.first()
        .unwanted_ingredients.values_list("id", flat=True)
    )
    assert sorted(stored) == sorted(ing_ids)


@pytest.mark.django_db
def test_create_order_invalid_payload(api_client, customer, restaurant):
    api_client.force_authenticate(user=customer.user)
    resp = api_client.post(
        "/order/new/",
        data=json.dumps({}),
        content_type="application/json",
    )
    assert resp.status_code == 400


@pytest.mark.django_db
def test_create_order_invalid_quantity_type(api_client, customer, restaurant, burger_item):
    api_client.force_authenticate(user=customer.user)
    payload = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [{"item_id": burger_item.pk, "quantity": "two"}],
    }
    resp = api_client.post(
        "/order/new/",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert resp.status_code == 400


@pytest.mark.django_db
def test_create_order_unauthenticated(api_client, customer, restaurant, burger_item):
    payload = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [{"item_id": burger_item.pk, "quantity": 1}],
    }
    resp = api_client.post(
        "/order/new/",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert resp.status_code == 401


# ------------------------------------------------------------------
# ETA/Status fields rounding tests
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_create_order_sets_eta_food_only(api_client, customer, restaurant, burger_item):
    burger_item.category = "Food"
    burger_item.save()
    api_client.force_authenticate(user=customer.user)

    now = timezone.now().replace(second=0, microsecond=0)
    payload = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [{"item_id": burger_item.pk, "quantity": 3}],
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
def test_create_order_sets_eta_beverage_only(api_client, customer, restaurant, burger_item):
    burger_item.category = "beverage"
    burger_item.save()
    api_client.force_authenticate(user=customer.user)

    now = timezone.now().replace(second=0, microsecond=0)
    payload = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [{"item_id": burger_item.pk, "quantity": 2}],
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


# ------------------------------------------------------------------
# GET /retrieve/orders/ - Manager views active orders
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_retrieve_active_orders_success(api_client, restaurant_with_user, customer, burger_item):
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    o = Order.objects.create(
        customer=customer, restaurant=restaurant, status="pending", total_price=0
    )
    OrderItem.objects.create(order=o, item=burger_item, quantity=1)

    resp = api_client.get("/retrieve/orders/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data["results"], list)
    assert any(r["id"] == o.id for r in data["results"])
    assert data["total"] >= 1
    assert data.get("next_offset") is None or isinstance(data["next_offset"], int)


@pytest.mark.django_db
def test_retrieve_active_orders_none_exist(api_client, restaurant_with_user):
    _, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    resp = api_client.get("/retrieve/orders/")
    assert resp.status_code == 200
    data = resp.json()
    assert data["results"] == []
    assert data["total"] == 0
    assert data.get("next_offset") is None


@pytest.mark.django_db
def test_retrieve_active_orders_unauthorized(api_client):
    u = CustomUser.objects.create_user(
        username="u", email="u@example.com", password="pass"
    )
    api_client.force_authenticate(user=u)
    resp = api_client.get("/retrieve/orders/")
    assert resp.status_code == 403


# ------------------------------------------------------------------
# PATCH /orders/<rest_id>/<order_id>/<new_status>/
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_update_order_status_requires_auth(api_client):
    resp = api_client.patch("/orders/1/1/completed/", data={}, format="json")
    assert resp.status_code == 401


@pytest.mark.django_db
def test_update_order_status_non_restaurant(api_client, customer, restaurant, burger_item):
    api_client.force_authenticate(user=customer.user)
    o = Order.objects.create(
        customer=customer, restaurant=restaurant, status="pending", total_price=0
    )
    resp = api_client.patch(
        f"/orders/{restaurant.pk}/{o.id}/completed/", data={}, format="json"
    )
    assert resp.status_code == 200


@pytest.mark.django_db
def test_update_order_status_invalid_status(api_client, restaurant_with_user, customer, burger_item):
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    o = Order.objects.create(customer=customer, restaurant=restaurant)
    resp = api_client.patch(
        f"/orders/{restaurant.pk}/{o.id}/unknown/", data={}, format="json"
    )
    assert resp.status_code == 400
    assert "invalid status" in resp.json()["error"].lower()


@pytest.mark.django_db
def test_update_order_status_in_progress_missing_worker(api_client, restaurant_with_user, customer, burger_item):
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    o = Order.objects.create(
        customer=customer, restaurant=restaurant, status="pending", total_price=0
    )
    resp = api_client.patch(
        f"/orders/{restaurant.pk}/{o.id}/in_progress/", data={}, format="json"
    )
    assert resp.status_code == 400
    assert "missing worker" in resp.json()["error"].lower()


@pytest.mark.django_db
def test_update_order_status_in_progress_success(api_client, restaurant_with_user, customer, burger_item):
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    worker = Worker.objects.create(restaurant=restaurant, name="W", pin="0000", role="staff")
    o = Order.objects.create(
        customer=customer, restaurant=restaurant, status="pending", total_price=0
    )
    resp = api_client.patch(
        f"/orders/{restaurant.pk}/{o.id}/in_progress/", data={"worker_id": worker.id}, format="json"
    )
    assert resp.status_code == 200
    js = resp.json()
    assert js["status"] == "in_progress"


@pytest.mark.django_db
def test_update_order_status_completed_updates_times_ordered(api_client, restaurant_with_user, customer, burger_item):
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    o = Order.objects.create(
        customer=customer, restaurant=restaurant, status="pending", total_price=0
    )
    OrderItem.objects.create(order=o, item=burger_item, quantity=2)
    initial = burger_item.times_ordered
    resp = api_client.patch(
        f"/orders/{restaurant.pk}/{o.id}/completed/", data={}, format="json"
    )
    assert resp.status_code == 200
    burger_item.refresh_from_db()
    assert burger_item.times_ordered == initial + 2


# ------------------------------------------------------------------
# PATCH /orders/<rest_id>/<order_id>/<category>/<new_status>/
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_update_order_category_invalid_category(api_client, restaurant_with_user):
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    resp = api_client.patch(f"/orders/{restaurant.pk}/1/invalid/completed/", data={}, format="json")
    assert resp.status_code == 400


@pytest.mark.django_db
def test_update_order_category_invalid_status(api_client, restaurant_with_user, customer, burger_item):
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    o = Order.objects.create(customer=customer, restaurant=restaurant)
    OrderItem.objects.create(order=o, item=burger_item, quantity=1)
    resp = api_client.patch(
        f"/orders/{restaurant.pk}/{o.id}/food/unknown/", data={}, format="json"
    )
    assert resp.status_code == 400


@pytest.mark.django_db
def test_update_order_category_success(api_client, restaurant_with_user, customer, burger_item):
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    o = Order.objects.create(customer=customer, restaurant=restaurant)
    OrderItem.objects.create(order=o, item=burger_item, quantity=1)
    resp = api_client.patch(
        f"/orders/{restaurant.pk}/{o.id}/food/completed/", data={}, format="json"
    )
    assert resp.status_code == 200
    js = resp.json()
    assert js["food_status"] == "completed"


# ------------------------------------------------------------------
# GET /order/customer/ and GET /order/<id>/
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_get_customer_orders_unauthenticated(api_client):
    resp = api_client.get("/order/customer/")
    assert resp.status_code == 401


@pytest.mark.django_db
def test_get_customer_orders_not_customer(api_client):
    u = CustomUser.objects.create_user(username="nc", email="nc@example.com", password="p")
    api_client.force_authenticate(user=u)
    resp = api_client.get("/order/customer/")
    assert resp.status_code == 404


@pytest.mark.django_db
def test_get_customer_orders_success(api_client, customer, restaurant, burger_item):
    api_client.force_authenticate(user=customer.user)
    o = Order.objects.create(customer=customer, restaurant=restaurant)
    OrderItem.objects.create(order=o, item=burger_item, quantity=1)
    resp = api_client.get("/order/customer/")
    assert resp.status_code == 200
    assert any(x["id"] == o.id for x in resp.json())


@pytest.mark.django_db
def test_get_order_not_found(api_client, customer):
    api_client.force_authenticate(user=customer.user)
    resp = api_client.get("/order/9999/")
    assert resp.status_code == 404


@pytest.mark.django_db
def test_get_order_success(api_client, customer, restaurant, burger_item):
    api_client.force_authenticate(user=customer.user)
    o = Order.objects.create(customer=customer, restaurant=restaurant)
    OrderItem.objects.create(order=o, item=burger_item, quantity=1)
    resp = api_client.get(f"/order/{o.id}/")
    assert resp.status_code == 200
    assert resp.json()["id"] == o.id


# ------------------------------------------------------------------
# POST /order/estimate/ - Customer requests ETA estimate
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_estimate_missing_params(api_client):
    resp = api_client.post(
        "/order/estimate/", data=json.dumps({}), content_type="application/json"
    )
    assert resp.status_code == 401


@pytest.mark.django_db
def test_estimate_invalid_item(api_client, customer, restaurant):
    api_client.force_authenticate(user=customer.user)
    data = {"restaurant_id": restaurant.id, "order_items": [{"item_id": 999, "quantity": 1}]}
    resp = api_client.post(
        "/order/estimate/", data=json.dumps(data), content_type="application/json"
    )
    assert resp.status_code == 400


@pytest.mark.django_db
def test_estimate_success(api_client, customer, restaurant, burger_item):
    burger_item.category = "Food"
    burger_item.save()
    bev = Item.objects.create(
        restaurant=restaurant,
        name="Soda",
        description="",
        price=Decimal("1.00"),
        category="beverage",
        stock=5,
        available=True,
    )
    api_client.force_authenticate(user=customer.user)
    data = {
        "restaurant_id": restaurant.id,
        "order_items": [
            {"item_id": burger_item.id, "quantity": 2},
            {"item_id": bev.id, "quantity": 3},
        ],
    }
    resp = api_client.post(
        "/order/estimate/", data=json.dumps(data), content_type="application/json"
    )
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body.get("food_eta_minutes"), int)
    assert isinstance(body.get("beverage_eta_minutes"), int)
    assert "estimated_food_ready_time" in body
    assert "estimated_beverage_ready_time" in body
