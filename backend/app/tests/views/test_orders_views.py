import json
from decimal import Decimal

import pytest
from app.models import CustomUser
from app.models.order_models import Order, OrderItem
from app.models.restaurant_models import Ingredient, Item
from django.utils import timezone


@pytest.fixture
def restaurant_with_user(restaurant):
    user = CustomUser.objects.create_user(username="mgruser", email="mgr@example.com", password="pass")
    restaurant.user = user
    restaurant.save()
    return restaurant, user


# ------------------------------------------------------------------
# POST /order/new/ - Create a new order
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_create_order_success(api_client, customer, restaurant, item):
    """
    Creates an order with one item. Should return 201 and success message.
    """
    api_client.force_authenticate(user=customer.user)
    data = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [{"item_id": item.pk, "quantity": 2}]
    }
    response = api_client.post("/order/new/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 201
    assert response.json().get("message") == "Order created successfully"


@pytest.mark.django_db
def test_create_order_with_unwanted_ingredients(api_client, customer, restaurant, item):
    """
    Creates an order and stores unwanted ingredients in the order item.
    """
    ing1 = Ingredient.objects.create(item=item, name="Pickles")
    ing2 = Ingredient.objects.create(item=item, name="Onions")
    api_client.force_authenticate(user=customer.user)

    data = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [{
            "item_id": item.pk,
            "quantity": 1,
            "unwanted_ingredients": [ing1.pk, ing2.pk]
        }]
    }
    response = api_client.post("/order/new/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 201
    order = Order.objects.get(pk=response.json()["order_id"])
    unwanted = list(order.order_items.first().unwanted_ingredients.values_list("id", flat=True))
    assert sorted(unwanted) == sorted([ing1.pk, ing2.pk])


@pytest.mark.django_db
def test_create_order_sets_eta_food_only(api_client, customer, restaurant, item):
    """
    Test order creation with food items only.
    With 3 food items (food ETA = 15 + 2*3 = 21 minutes, rounds to 25 minutes),
    the order's estimated_pickup_time should be roughly 25 minutes in the future.
    """
    # Ensure the item is considered food (its category is not "beverage")
    item.category = "Food"
    item.save()

    api_client.force_authenticate(user=customer.user)
    data = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [{"item_id": item.pk, "quantity": 3}]
    }
    response = api_client.post("/order/new/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 201, f"Response data: {response.json()}"

    # Retrieve the order and verify that ETA is set
    order = Order.objects.get(pk=response.json()["order_id"])
    assert order.estimated_pickup_time is not None, "ETA not set for food-only order."

    now = timezone.now()
    expected_eta = now + timezone.timedelta(minutes=25)
    delta = order.estimated_pickup_time - expected_eta
    # Allow a small difference (up to 2 minutes) due to processing time
    assert abs(delta.total_seconds()) < 120, f"ETA off by {delta.total_seconds()} seconds"


@pytest.mark.django_db
def test_create_order_sets_eta_beverage_only(api_client, customer, restaurant, item):
    """
    Test order creation with beverage items only.
    For beverage-only orders:
      - Beverage ETA = beverage quantity * 1 minute each.
      - Food ETA = base time (15 minutes) since there are no food items.
    Overall ETA will be max(15, beverage ETA), rounded to nearest 5.

    For example, if 2 beverages are ordered:
      Beverage ETA = 2 minutes, but overall ETA = max(15,2) = 15 minutes.
    If 20 beverages are ordered:
      Beverage ETA = 20 minutes, overall ETA = 20 minutes (rounded to 20).
    """
    # Set the item as a beverage.
    item.category = "beverage"  # Lowercase is preferred.
    item.save()
    api_client.force_authenticate(user=customer.user)

    # Test with 2 beverages:
    data = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [{"item_id": item.pk, "quantity": 2}]
    }
    response = api_client.post("/order/new/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 201, f"Response: {response.json()}"
    order = Order.objects.get(pk=response.json()["order_id"])
    assert order.estimated_pickup_time is not None, "ETA not set for beverage-only order."

    now = timezone.now()
    # With 2 beverages: beverage ETA = 2 minutes, food ETA = 15 minutes => Overall ETA = max(15,2)=15.
    expected_eta = now + timezone.timedelta(minutes=15)
    delta = order.estimated_pickup_time - expected_eta
    assert abs(delta.total_seconds()) < 120, f"Beverage-only ETA off by {delta.total_seconds()} seconds"

    # Test with 20 beverages:
    data = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [{"item_id": item.pk, "quantity": 20}]
    }
    response = api_client.post("/order/new/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 201, f"Response: {response.json()}"
    order = Order.objects.get(pk=response.json()["order_id"])

    now = timezone.now()
    # With 20 beverages: beverage ETA = 20 minutes, food ETA = 15 minutes, so overall ETA = max(20,15)=20.
    # Rounded to nearest 5 (20 is already a multiple of 5).
    expected_eta = now + timezone.timedelta(minutes=20)
    delta = order.estimated_pickup_time - expected_eta
    assert abs(delta.total_seconds()) < 120, f"Beverage-only (20 items) ETA off by {delta.total_seconds()} seconds"


@pytest.mark.django_db
def test_create_order_sets_eta_mixed(api_client, customer, restaurant, burger_item):
    """
    Test order creation for an order with both food and beverages.
    Create one food item and one beverage item.

    Food ETA for 1 food item: 15 + 2*1 = 17 minutes.
    For beverages: we'll simulate a beverage order by creating a new item with category "beverage".
    With 10 beverages at 1 minute each and an empty scheduler,
    beverage ETA = 10 minutes.
    Overall ETA is max(17, 10) = 17, rounded to the nearest 5 = 20 minutes.
    """
    from app.models.restaurant_models import Item

    # Make sure burger_item remains food.
    burger_item.category = "Food"
    burger_item.save()

    # Create a beverage item for this restaurant.
    beverage_item = Item.objects.create(
        restaurant=restaurant,
        name="Test beverage",
        description="A refreshing beverage",
        price=Decimal("3.50"),
        category="beverage",  # Ensure lower-case "beverage" so the view treats it as a beverage order.
        stock=50,
        available=True,
        base64_image="beverage-image"
    )

    api_client.force_authenticate(user=customer.user)
    data = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [
            {"item_id": burger_item.pk, "quantity": 1},
            {"item_id": beverage_item.pk, "quantity": 10}
        ]
    }
    response = api_client.post("/order/new/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 201, f"Response data: {response.json()}"

    order = Order.objects.get(pk=response.json()["order_id"])
    assert order.estimated_pickup_time is not None, "ETA not set for mixed order."

    # Expected calculations:
    # Food ETA = 15 + (2*1) = 17 minutes.
    # beverage ETA = 10 * 1 = 10 minutes (scheduler has no pre-existing orders).
    # Overall ETA = max(17,10) = 17, which rounds to 20 minutes.
    now = timezone.now()
    expected_eta = now + timezone.timedelta(minutes=20)
    delta = order.estimated_pickup_time - expected_eta
    assert abs(delta.total_seconds()) < 120, f"ETA off by {delta.total_seconds()} seconds"


@pytest.mark.django_db
def test_create_order_invalid_data(api_client, customer, restaurant):
    """
    Omits order_items from payload. Should return 400.
    """
    api_client.force_authenticate(user=customer.user)
    data = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk
    }
    response = api_client.post("/order/new/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_order_invalid_quantity_type(api_client, customer, restaurant, item):
    """
    Passes quantity as string instead of integer. Should return 400.
    """
    api_client.force_authenticate(user=customer.user)
    data = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [{"item_id": item.pk, "quantity": "two"}]
    }
    response = api_client.post("/order/new/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400


@pytest.mark.django_db
def test_create_order_unauthenticated(api_client, customer, restaurant):
    """
    Unauthenticated user should receive 401 when placing order.
    """
    data = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": []
    }
    response = api_client.post("/order/new/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 401


# ------------------------------------------------------------------
# GET /retrieve/orders/ - Manager views active orders
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_retrieve_active_orders_success(api_client, restaurant_with_user, customer, item):
    """
    Manager should receive list of active orders for their restaurant.
    """
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)

    order = Order.objects.create(customer=customer, restaurant=restaurant, status="pending", total_price=0)
    OrderItem.objects.create(order=order, item=item, quantity=1)

    response = api_client.get("/retrieve/orders/")
    assert response.status_code == 200
    data = response.json()
    assert any(o["id"] == order.id for o in data)


@pytest.mark.django_db
def test_retrieve_active_orders_none_exist(api_client, restaurant_with_user):
    """
    Restaurant has no active orders. Should return an empty list.
    """
    _, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    response = api_client.get("/retrieve/orders/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.django_db
def test_retrieve_active_orders_unauthorized(api_client):
    """
    User without linked restaurant should receive 403.
    """
    user = CustomUser.objects.create_user(username="unauth", email="unauth@example.com", password="pass")
    api_client.force_authenticate(user=user)
    response = api_client.get("/retrieve/orders/")
    assert response.status_code == 403


# ------------------------------------------------------------------
# PATCH /orders/<id>/complete/ - Mark an order as completed
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_mark_order_completed_success(api_client, restaurant_with_user, customer, item):
    """
    Marks an order as completed. Should return 200 and update status.
    """
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)

    order = Order.objects.create(customer=customer, restaurant=restaurant, status="pending", total_price=0)
    response = api_client.patch(f"/orders/{order.id}/completed/", data={}, format="json")
    assert response.status_code == 200
    order.refresh_from_db()
    assert order.status == "completed"


@pytest.mark.django_db
def test_mark_order_completed_not_found(api_client, restaurant_with_user):
    """
    Tries to complete a non-existent order. Should return 404.
    """
    _, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    response = api_client.patch("/orders/9999/completed/", data={}, format="json")
    assert response.status_code == 404


# ------------------------------------------------------------------
# GET /order/customer/ - Customer views their own orders
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_get_customer_orders_success(api_client, customer, restaurant, item):
    """
    Customer should receive list of their own orders.
    """
    api_client.force_authenticate(user=customer.user)
    order = Order.objects.create(customer=customer, restaurant=restaurant, status="pending", total_price=0)
    OrderItem.objects.create(order=order, item=item, quantity=1)
    response = api_client.get("/order/customer/")
    assert response.status_code == 200
    assert any(o["id"] == order.id for o in response.json())


@pytest.mark.django_db
def test_get_customer_orders_none_exist(api_client, customer):
    """
    Customer with no orders should get an empty list.
    """
    api_client.force_authenticate(user=customer.user)
    response = api_client.get("/order/customer/")
    assert response.status_code == 200
    assert response.json() == []


@pytest.mark.django_db
def test_get_customer_orders_not_customer(api_client):
    """
    Non-customer user should receive 404 on customer orders endpoint.
    """
    user = CustomUser.objects.create_user(username="notcust", email="x@example.com", password="pass")
    api_client.force_authenticate(user=user)
    response = api_client.get("/order/customer/")
    assert response.status_code == 404


# ------------------------------------------------------------------
# POST order/estimate/ - Customer requests order ETA estimate
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_estimate_order_eta_food_only(api_client, customer, restaurant, item):
    """
    Test order ETA estimation with food items only.
    """
    item.category = "Food"
    item.save()
    api_client.force_authenticate(user=customer.user)
    data = {"restaurant_id": restaurant.id, "order_items": [{"item_id": item.id, "quantity": 4}]}
    resp = api_client.post("/order/estimate/", data=json.dumps(data), content_type="application/json")
    assert resp.status_code == 200
    body = resp.json()
    # food ETA = 15 + 2*4 = 23 → round to 25
    assert body["eta_minutes"] == 25


@pytest.mark.django_db
def test_estimate_order_eta_beverage_only(api_client, customer, restaurant, item):
    """
    Test order ETA estimation with beverage items only.
    """
    item.category = "beverage"
    item.save()
    api_client.force_authenticate(user=customer.user)
    data = {"restaurant_id": restaurant.id, "order_items": [{"item_id": item.id, "quantity": 3}]}
    resp = api_client.post("/order/estimate/", data=json.dumps(data), content_type="application/json")
    assert resp.status_code == 200
    body = resp.json()
    # beverage ETA = 3, food ETA = 15 → overall 15
    assert body["eta_minutes"] == 15


@pytest.mark.django_db
def test_estimate_order_eta_mixed(api_client, customer, restaurant, burger_item):
    """
    Test order ETA estimation with mixed items.
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
            {"item_id": burger_item.id, "quantity": 2},  # food ETA=15+4=19→20
            {"item_id": bev.id, "quantity": 5}  # bev ETA=5
        ]
    }
    resp = api_client.post("/order/estimate/", data=json.dumps(data), content_type="application/json")
    assert resp.status_code == 200
    assert resp.json()["eta_minutes"] == 20
