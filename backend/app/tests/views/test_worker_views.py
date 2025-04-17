import json

import pytest
from app.models.worker_models import Worker


# ------------------------------------------------------------------
# POST /create-worker/ - Create a new worker for a restaurant
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_create_worker_success(api_client, restaurant):
    """
    A valid request should create a worker and return 201 with worker ID.
    """
    data = {
        "pin": "9999",
        "role": "bartender",
        "restaurant_id": restaurant.id
    }
    response = api_client.post("/create-worker/", data=json.dumps(data), content_type="application/json")

    assert response.status_code == 201
    resp = response.json()
    assert resp["message"] == "Bartender created successfully"
    assert "worker_id" in resp

    worker = Worker.objects.get(id=resp["worker_id"])
    assert worker.pin == "9999"
    assert worker.role == "bartender"
    assert worker.restaurant == restaurant


@pytest.mark.django_db
def test_create_worker_missing_fields(api_client, restaurant):
    """
    Omitting required fields should return 400 with a validation error.
    """
    data = {
        "pin": "1234",
        # missing role and restaurant_id
    }
    response = api_client.post("/create-worker/", data=json.dumps(data), content_type="application/json")

    assert response.status_code == 400
    assert "Missing required fields" in response.json()["error"]


@pytest.mark.django_db
def test_create_worker_duplicate_pin(api_client, restaurant):
    """
    Creating a worker with a duplicate pin for the same restaurant should fail with 400.
    """
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
    """
    Request with non-existent restaurant ID should return 404.
    """
    data = {
        "pin": "1234",
        "role": "manager",
        "restaurant_id": 9999  # invalid ID
    }
    response = api_client.post("/create-worker/", data=json.dumps(data), content_type="application/json")

    assert response.status_code == 404
    assert "Restaurant not found" in response.json()["error"]


@pytest.mark.django_db
def test_create_worker_invalid_method(api_client):
    """
    GET request to /create-worker/ should return 400.
    """
    response = api_client.get("/create-worker/")
    assert response.status_code == 400
    assert "Invalid request" in response.json()["error"]
