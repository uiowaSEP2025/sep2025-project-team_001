import json

import pytest
from app.models.restaurant_models import Restaurant
from app.models.worker_models import Worker


@pytest.mark.django_db
def test_create_worker_success(api_client, restaurant):
    data = {
        "pin": "9999",
        "role": "bartender",
        "restaurant_id": restaurant.id
    }
    response = api_client.post("/create-worker/", data=json.dumps(data), content_type="application/json")

    assert response.status_code == 201
    resp = response.json()
    assert "worker_id" in resp
    assert resp["message"] == "Bartender created successfully"
    worker = Worker.objects.get(id=resp["worker_id"])
    assert worker.role == "bartender"
    assert worker.pin == "9999"


@pytest.mark.django_db
def test_create_worker_missing_fields(api_client, restaurant):
    data = {
        "pin": "1234",
        # missing role and restaurant_id
    }
    response = api_client.post("/create-worker/", data=json.dumps(data), content_type="application/json")

    assert response.status_code == 400
    assert "Missing required fields" in response.json()["error"]


@pytest.mark.django_db
def test_create_worker_duplicate_pin(api_client, restaurant):
    Worker.objects.create(pin="1234", role="manager", restaurant=restaurant)

    data = {
        "pin": "1234",
        "role": "bartender",
        "restaurant_id": restaurant.id
    }
    response = api_client.post("/create-worker/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert "PIN already in use" in response.json()["error"]


@pytest.mark.django_db
def test_create_worker_invalid_restaurant(api_client):
    data = {
        "pin": "1234",
        "role": "manager",
        "restaurant_id": 9999  # does not exist
    }
    response = api_client.post("/create-worker/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 404
    assert "Restaurant not found" in response.json()["error"]


@pytest.mark.django_db
def test_create_worker_invalid_method(api_client):
    response = api_client.get("/create-worker/")
    assert response.status_code == 400
    assert "Invalid request" in response.json()["error"]
