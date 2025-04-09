import json

import pytest
from app.models import CustomUser
from app.models.order_models import Order, OrderItem
from app.models.restaurant_models import Ingredient


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
    response = api_client.patch(f"/orders/{order.id}/complete/", data={}, format="json")
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
    response = api_client.patch("/orders/9999/complete/", data={}, format="json")
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
