import json

import pytest
from app.models.customer_models import CustomUser
from app.models.order_models import Order
from app.models.restaurant_models import Restaurant
from app.models.review_models import Review
from app.models.worker_models import Worker


# ------------------------------------------------------------------
# POST /mobile/review/create - create_review view
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_create_review_unauthenticated(api_client, order):
    payload = {"order": order.id, "rating": 5, "comment": "Great"}
    resp = api_client.post("/mobile/review/create", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 401


@pytest.mark.django_db
def test_create_review_default_rating(api_client, restaurant, customer, order):
    # Authenticate as the restaurant user
    api_client.force_authenticate(user=restaurant.user)

    # Ensure a worker is present for the order (to satisfy serializer)
    w = Worker.objects.create(restaurant=restaurant, pin="0000", role="bartender", name="Bob")
    order.worker = w
    order.save()

    payload = {"order": order.id, "comment": "Ok service"}
    resp = api_client.post("/mobile/review/create", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 201
    data = resp.json()
    assert data["rating"] == 5
    assert data["comment"] == "Ok service"

    # And the order should be marked reviewed
    order.refresh_from_db()
    assert order.reviewed is True


@pytest.mark.django_db
def test_create_review_success(api_client, restaurant, customer, order):
    # add worker to order
    order.worker = Worker.objects.create(restaurant=restaurant, pin="3333", role="bartender", name="W")
    order.save()
    api_client.force_authenticate(user=restaurant.user)
    payload = {"order": order.id, "rating": 4, "comment": "Nice"}
    resp = api_client.post("/mobile/review/create", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 201
    data = resp.json()
    assert data["order"] == order.id
    assert data["rating"] == 4
    assert data["comment"] == "Nice"
    # order.reviewed should be True
    order.refresh_from_db()
    assert order.reviewed is True


@pytest.mark.django_db
def test_create_review_duplicate(api_client, restaurant, customer, order):
    api_client.force_authenticate(user=restaurant.user)
    # first review
    Review.objects.create(order=order, rating=3, comment="First")
    payload = {"order": order.id, "rating": 5, "comment": "Again"}
    resp = api_client.post("/mobile/review/create", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 400
    assert resp.json()["error"] == "Review already exists for this order."


# ------------------------------------------------------------------
# GET /reviews/ - list_reviews view
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_list_reviews_unauthenticated(api_client):
    resp = api_client.get("/reviews/")
    assert resp.status_code == 401


@pytest.mark.django_db
def test_list_reviews_non_restaurant(api_client, custom_user):
    api_client.force_authenticate(user=custom_user)
    resp = api_client.get("/reviews/")
    assert resp.status_code == 403
    assert "Only restaurant accounts" in resp.json()["error"]


@pytest.mark.django_db
def test_list_reviews_success(api_client, restaurant, customer, order):
    api_client.force_authenticate(user=restaurant.user)
    # create reviews for this and other restaurant
    r1 = Review.objects.create(order=order, rating=5, comment="Good")
    # other restaurant
    other_user = CustomUser.objects.create_user(username="u2", email="u2@e.com", password="p")
    other_rest = Restaurant.objects.create(user=other_user, name="O", address="A", phone="P")
    o2 = Order.objects.create(customer=customer, restaurant=other_rest, total_price=0)
    Review.objects.create(order=o2, rating=2, comment="Bad")
    resp = api_client.get("/reviews/")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, list)
    assert any(rv["id"] == r1.id for rv in data)
    # ensure other review not included
    assert all(rv["order"] == order.id for rv in data)
