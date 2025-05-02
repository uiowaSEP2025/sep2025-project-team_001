import json

import pytest
from app.models.worker_models import Worker


# ------------------------------------------------------------------
# POST /create-worker/ - Create a new worker for a restaurant
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_create_worker_success(auth_client, restaurant):
    """
    A valid request should create a worker and return 201 with worker ID.
    """
    data = {
        "pin": "9999",
        "role": "bartender",
        "name": "John Doe",
        "restaurant_id": restaurant.id
    }
    response = auth_client.post("/create-worker/", data=json.dumps(data), content_type="application/json")

    assert response.status_code == 201
    resp = response.json()
    assert resp["message"] == "Bartender created successfully"
    assert "worker_id" in resp

    worker = Worker.objects.get(id=resp["worker_id"])
    assert worker.pin == "9999"
    assert worker.role == "bartender"
    assert worker.name == "John Doe"
    assert worker.restaurant == restaurant


@pytest.mark.django_db
def test_create_worker_missing_fields(auth_client, restaurant):
    """
    Omitting required fields should return 400 with a validation error.
    """
    data = {
        "pin": "1234",
        # missing role and restaurant_id
    }
    response = auth_client.post("/create-worker/", data=json.dumps(data), content_type="application/json")

    assert response.status_code == 400
    assert "Missing required fields" in response.json()["error"]


@pytest.mark.django_db
def test_create_worker_duplicate_pin(auth_client, restaurant):
    """
    Creating a worker with a duplicate pin for the same restaurant should fail with 400.
    """
    Worker.objects.create(pin="1234", role="manager", restaurant=restaurant)

    data = {
        "pin": "1234",
        "role": "bartender",
        "name": "John Doe",
        "restaurant_id": restaurant.id
    }
    response = auth_client.post("/create-worker/", data=json.dumps(data), content_type="application/json")

    assert response.status_code == 400
    assert "PIN already in use" in response.json()["error"]


@pytest.mark.django_db
def test_create_worker_invalid_restaurant(auth_client):
    """
    Request with non-existent restaurant ID should return 404.
    """
    data = {
        "pin": "1234",
        "role": "manager",
        "name": "John Doe",
        "restaurant_id": 9999  # invalid ID
    }
    response = auth_client.post("/create-worker/", data=json.dumps(data), content_type="application/json")

    assert response.status_code == 404
    assert "Restaurant not found" in response.json()["error"]
