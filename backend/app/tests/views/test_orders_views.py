import json
from decimal import Decimal
import pytest
from rest_framework.test import APIClient
from app.models import CustomUser, Customer
from app.models.restaurant_models import Restaurant, Item
from app.models.order_models import Order, OrderItem


# --- Fixtures ---

@pytest.fixture
def api_client():
    return APIClient()


# Use the existing conftest manager fixture (if not available, this creates one)
@pytest.fixture
def manager_user():
    user = CustomUser.objects.create_user(username="manager_for_order", email="manager_for_order@example.com",
                                          password="pass")
    from app.models.customer_models import Manager  # Import here to avoid circular import issues
    manager = Manager.objects.create(user=user)
    # Create a restaurant and assign to manager.
    restaurant = Restaurant.objects.create(
        name="Manager's Restaurant",
        address="456 Manager St",
        phone="111-222-3333",
        restaurant_image="manager_dummy"
    )
    restaurant.managers.add(manager)
    return user


@pytest.fixture
def manager_client(api_client, manager_user):
    api_client.force_authenticate(user=manager_user)
    return api_client


@pytest.fixture
def customer_user():
    user = CustomUser.objects.create_user(username="order_customer", email="order_customer@example.com",
                                          password="pass")
    return user


@pytest.fixture
def customer(customer_user):
    return Customer.objects.create(user=customer_user)


# Create a restaurant for customer orders (if needed)
@pytest.fixture
def customer_restaurant():
    # For orders created by a customer, the restaurant can be any valid restaurant.
    return Restaurant.objects.create(
        name="Customer Restaurant",
        address="789 Customer Ave",
        phone="444-555-6666",
        restaurant_image="customer_dummy"
    )


# --- Tests for create_order ---

@pytest.mark.django_db
def test_create_order_success(api_client, customer, customer_restaurant, item):
    """
    Test that a valid POST to /order/new/ creates an order with nested OrderItems.
    """
    # Authenticate as any user (create_order does not require authentication).
    api_client.force_authenticate(user=customer.user)
    data = {
        "customer_id": customer.pk,
        "restaurant_id": customer_restaurant.pk,
        "order_items": [
            {"item_id": item.pk, "quantity": 2}
        ]
    }
    response = api_client.post("/order/new/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 201, response.content
    resp_data = response.json()
    assert resp_data.get("message") == "Order created successfully"
    assert "order_id" in resp_data


@pytest.mark.django_db
def test_create_order_invalid_data(api_client, customer, customer_restaurant):
    """
    Test that an invalid POST to /order/new/ (missing order_items) returns a 400 error.
    """
    api_client.force_authenticate(user=customer.user)
    data = {
        "customer_id": customer.pk,
        "restaurant_id": customer_restaurant.pk,
        # Missing "order_items"
    }
    response = api_client.post("/order/new/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400, response.content


@pytest.mark.django_db
def test_create_order_unauthenticated(api_client, customer, customer_restaurant):
    """
    Test that an unauthenticated POST to /order/new/ returns a 401 Unauthorized error.
    """
    data = {
        "customer_id": customer.pk,
        "restaurant_id": customer_restaurant.pk,
        "order_items": []
    }
    response = api_client.post("/order/new/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 401, response.content


# --- Tests for retrieve_active_orders ---

@pytest.mark.django_db
def test_retrieve_active_orders_success(manager_client, manager_user):
    """
    Test that an authenticated manager can retrieve active orders for their restaurant.
    """
    # Get manager's restaurant.
    from app.models.customer_models import Manager
    manager = manager_user.manager
    restaurant = manager.restaurants.first()
    # Create a customer and an order for this restaurant.
    cust_user = CustomUser.objects.create_user(username="cust1", email="cust1@example.com", password="pass")
    cust = Customer.objects.create(user=cust_user)
    order = Order.objects.create(
        customer=cust,
        restaurant=restaurant,
        status="pending",
        total_price=Decimal("0.00")
    )
    # Create an OrderItem for the order.
    item = Item.objects.create(
        restaurant=restaurant,
        name="Active Item",
        description="For active order test",
        price=Decimal("10.00"),
        category="Food",
        stock=5,
        available=True,
        base64_image="active_dummy"
    )
    OrderItem.objects.create(order=order, item=item, quantity=3)

    response = manager_client.get("/retrieve/orders/")
    assert response.status_code == 200, response.content
    data = response.json()
    # Expect a list of orders.
    assert isinstance(data, list)
    order_ids = [o["id"] for o in data]
    assert order.id in order_ids


@pytest.mark.django_db
def test_retrieve_active_orders_no_manager(api_client):
    """
    Test that a user who is not a manager gets a 404 when trying to retrieve active orders.
    """
    # Create a non-manager user.
    user = CustomUser.objects.create_user(username="nonmanager", email="nonmanager@example.com", password="pass")
    client = APIClient()
    client.force_authenticate(user=user)
    response = client.get("/retrieve/orders/")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data


# --- Tests for mark_order_completed ---

@pytest.mark.django_db
def test_mark_order_completed_success(manager_client, manager_user):
    """
    Test that a manager can mark an order as completed.
    """
    manager = manager_user.manager
    restaurant = manager.restaurants.first()
    # Create a customer and an order.
    cust_user = CustomUser.objects.create_user(username="cust_mark", email="cust_mark@example.com", password="pass")
    cust = Customer.objects.create(user=cust_user)
    order = Order.objects.create(
        customer=cust,
        restaurant=restaurant,
        status="pending",
        total_price=Decimal("0.00")
    )
    order_id = order.id
    url = f"/orders/{order_id}/complete/"
    response = manager_client.patch(url, data={}, format="json")
    assert response.status_code == 200, response.content
    data = response.json()
    assert data.get("message") == "Order marked as completed."
    order.refresh_from_db()
    assert order.status == "completed"


@pytest.mark.django_db
def test_mark_order_completed_not_found(manager_client):
    """
    Test that marking a non-existent order returns a 404 error.
    """
    response = manager_client.patch("/orders/9999/complete/", data={}, format="json")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data


# --- Tests for get_customer_orders ---

@pytest.mark.django_db
def test_get_customer_orders_success(api_client, customer, customer_restaurant):
    """
    Test that an authenticated customer can retrieve their orders.
    """
    client = APIClient()
    client.force_authenticate(user=customer.user)
    # Create an order for this customer.
    order = Order.objects.create(
        customer=customer,
        restaurant=customer_restaurant,
        status="pending",
        total_price=Decimal("0.00")
    )
    item = Item.objects.create(
        restaurant=customer_restaurant,
        name="Cust Order Item",
        description="For customer order test",
        price=Decimal("15.00"),
        category="Food",
        stock=10,
        available=True,
        base64_image="cust_dummy"
    )
    OrderItem.objects.create(order=order, item=item, quantity=1)

    response = client.get("/order/customer/")
    assert response.status_code == 200, response.content
    data = response.json()
    assert isinstance(data, list)
    order_ids = [o["id"] for o in data]
    assert order.id in order_ids


@pytest.mark.django_db
def test_get_customer_orders_not_customer(api_client, manager_user):
    """
    Test that a user who is not a customer (e.g. a manager) gets a 404 error when accessing customer orders.
    """
    client = APIClient()
    client.force_authenticate(user=manager_user)
    response = client.get("/order/customer/")
    assert response.status_code == 404
    data = response.json()
    assert "error" in data
