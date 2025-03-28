import json
from decimal import Decimal

import pytest
from rest_framework.test import APIClient

from app.models import CustomUser
from app.models.restaurant_models import Restaurant, Item



@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def user():
    return CustomUser.objects.create_user(username="orderuser", email="orderuser@example.com", password="pass")


@pytest.fixture
def customer(user):
    from app.models.customer_models import Customer
    return Customer.objects.create(user=user)


@pytest.fixture
def restaurant():
    return Restaurant.objects.create(
        name="Testaurant",
        address="123 Main St",
        phone="555-555-5555",
        restaurant_image="dummyimage"
    )


@pytest.fixture
def item(restaurant):
    return Item.objects.create(
        restaurant=restaurant,
        name="Burger",
        description="Delicious burger",
        price=Decimal("9.99"),
        category="Food",
        stock=50,
        available=True,
        base64_image="dummyimage"
    )


@pytest.mark.django_db
def test_create_order_success(api_client, user, customer, restaurant, item):
    """
    Test that a valid POST request to /order/new creates an Order (with nested OrderItems)
    and returns a 201 response with the order ID.
    """
    # Authenticate the client.
    api_client.force_authenticate(user=user)

    # Prepare valid order data.
    data = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": [
            {"item_id": item.pk, "quantity": 2}
        ]
    }

    response = api_client.post("/order/new", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 201, response.content
    resp_data = response.json()
    assert resp_data.get("message") == "Order created successfully"
    assert "order_id" in resp_data


@pytest.mark.django_db
def test_create_order_invalid_data(api_client, user, customer, restaurant):
    """
    Test that an authenticated POST request with invalid data (e.g. missing order_items)
    returns a 400 error.
    """
    api_client.force_authenticate(user=user)
    data = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        # "order_items" is missing
    }
    response = api_client.post("/order/new", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400, response.content


@pytest.mark.django_db
def test_create_order_unauthenticated(api_client, customer, restaurant):
    """
    Test that an unauthenticated POST request to /order/new returns a 401 Unauthorized error.
    """
    # No authentication provided.
    data = {
        "customer_id": customer.pk,
        "restaurant_id": restaurant.pk,
        "order_items": []
    }
    response = api_client.post("/order/new", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 401, response.content
