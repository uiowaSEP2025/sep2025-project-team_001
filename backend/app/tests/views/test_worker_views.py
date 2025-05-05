import json

import pytest
from app.models import CustomUser, Restaurant
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
    response = auth_client.post(
        "/create-worker/", data=json.dumps(data), content_type="application/json"
    )

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
    data = {"pin": "1234"}  # missing role, name, restaurant_id
    response = auth_client.post(
        "/create-worker/", data=json.dumps(data), content_type="application/json"
    )

    assert response.status_code == 400
    assert "Missing required fields" in response.json()["error"]


@pytest.mark.django_db
def test_create_worker_duplicate_pin(auth_client, restaurant):
    """
    Creating a worker with a duplicate pin for the same restaurant should fail with 400.
    """
    # Pre-existing worker
    Worker.objects.create(pin="1234", role="manager", name="Mgr", restaurant=restaurant)

    data = {
        "pin": "1234",
        "role": "bartender",
        "name": "John Doe",
        "restaurant_id": restaurant.id
    }
    response = auth_client.post(
        "/create-worker/", data=json.dumps(data), content_type="application/json"
    )

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
        "restaurant_id": 9999
    }
    response = auth_client.post(
        "/create-worker/", data=json.dumps(data), content_type="application/json"
    )

    assert response.status_code == 404
    assert "Restaurant not found" in response.json()["error"]


@pytest.mark.django_db
def test_create_worker_unauthenticated(api_client, restaurant):
    """
    Unauthenticated user should get 401.
    """
    data = {
        "pin": "0000",
        "role": "bartender",
        "name": "Anon",
        "restaurant_id": restaurant.id
    }
    response = api_client.post(
        "/create-worker/", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 401


# ------------------------------------------------------------------
# GET /get-workers/ - List all workers for a restaurant
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_get_workers_success(manager_client, manager_user_with_worker):
    """
    Manager should see all workers for their restaurant.
    """
    restaurant = manager_user_with_worker["restaurant"]
    # Add a second worker
    w2 = Worker.objects.create(
        restaurant=restaurant, pin="1111", role="bartender", name="Second"
    )

    response = manager_client.get("/get-workers/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    ids = [w["id"] for w in data]
    assert manager_user_with_worker["worker"].id in ids
    assert w2.id in ids


@pytest.mark.django_db
def test_get_workers_no_auth(api_client):
    """
    Unauthenticated user should get 401.
    """
    response = api_client.get("/get-workers/")
    assert response.status_code == 401


@pytest.mark.django_db
def test_get_workers_non_restaurant(auth_client):
    """
    Authenticated user without a restaurant should get 403.
    """
    response = auth_client.get("/get-workers/")
    assert response.status_code == 403
    assert "Only restaurant accounts" in response.json()["error"]


# ------------------------------------------------------------------
# PUT /update-worker/<worker_id>/ - Update a worker's info
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_update_worker_success(manager_client, manager_user_with_worker):
    """
    Valid update should change name, pin, and role.
    """
    worker = manager_user_with_worker["worker"]
    url = f"/update-worker/{worker.id}/"
    payload = {"name": "New Name", "pin": "8888", "role": "bartender"}
    response = manager_client.put(
        url, data=json.dumps(payload), content_type="application/json"
    )
    assert response.status_code == 200
    resp = response.json()
    assert resp["message"] == "Worker updated successfully"

    w = Worker.objects.get(id=worker.id)
    assert w.name == "New Name"
    assert w.pin == "8888"
    assert w.role == "bartender"


@pytest.mark.django_db
def test_update_worker_not_found(manager_client):
    """
    Updating non-existent worker should return 404.
    """
    response = manager_client.put(
        "/update-worker/9999/", data=json.dumps({"name": "X"}), content_type="application/json"
    )
    assert response.status_code == 404
    assert "Worker not found" in response.json()["error"]


@pytest.mark.django_db
def test_update_worker_duplicate_pin(manager_client, manager_user_with_worker):
    """
    Changing a worker's pin to one already in use should fail 400.
    """
    restaurant = manager_user_with_worker["restaurant"]
    w1 = manager_user_with_worker["worker"]
    w2 = Worker.objects.create(
        restaurant=restaurant, pin="2222", role="bartender", name="Other"
    )
    response = manager_client.put(
        f"/update-worker/{w2.id}/",
        data=json.dumps({"pin": w1.pin}), content_type="application/json"
    )
    assert response.status_code == 400
    assert "PIN already in use" in response.json()["error"]


@pytest.mark.django_db
def test_update_worker_invalid_role(manager_client, manager_user_with_worker):
    """
    Providing an invalid role should return 400.
    """
    w = manager_user_with_worker["worker"]
    response = manager_client.put(
        f"/update-worker/{w.id}/", data=json.dumps({"role": "chef"}), content_type="application/json"
    )
    assert response.status_code == 400
    assert "Invalid role" in response.json()["error"]


# ------------------------------------------------------------------
# DELETE /delete-worker/<worker_id>/ - Remove a worker
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_delete_worker_success(manager_client, manager_user_with_worker):
    """
    Deleting a bartender should succeed.
    """
    restaurant = manager_user_with_worker["restaurant"]
    b = Worker.objects.create(
        restaurant=restaurant, pin="5555", role="bartender", name="ToDelete"
    )
    response = manager_client.delete(f"/delete-worker/{b.id}/")
    assert response.status_code == 200
    assert response.json()["message"] == "Worker deleted successfully"
    with pytest.raises(Worker.DoesNotExist):
        Worker.objects.get(id=b.id)


@pytest.mark.django_db
def test_delete_last_manager(manager_client, manager_user_with_worker):
    """
    Attempting to delete the only manager should return 400.
    """
    m = manager_user_with_worker["worker"]
    response = manager_client.delete(f"/delete-worker/{m.id}/")
    assert response.status_code == 400
    assert "At least one manager is required" in response.json()["error"]


@pytest.mark.django_db
def test_delete_worker_not_found(manager_client):
    """
    Deleting a non-existent worker should return 404.
    """
    response = manager_client.delete("/delete-worker/9999/")
    assert response.status_code == 404
    assert "Worker not found" in response.json()["error"]


@pytest.mark.django_db
def test_delete_worker_unauthorized(auth_client, manager_user_with_worker):
    """
    A logged-in user with no restaurant should get 403.
    """
    w = manager_user_with_worker["worker"]
    response = auth_client.delete(f"/delete-worker/{w.id}/")
    assert response.status_code == 403
    assert response.json()["error"] == "Unauthorized"


@pytest.mark.django_db
def test_delete_worker_other_restaurant(manager_client):
    """
    A manager from one restaurant cannot delete a worker from another.
    """
    other_user = CustomUser.objects.create_user("other", "o@x.com", "pw")
    other_rest = Restaurant.objects.create(user=other_user, name="Other", address="X", phone="P")
    other_worker = Worker.objects.create(restaurant=other_rest, pin="3333", role="manager", name="Someone")

    response = manager_client.delete(f"/delete-worker/{other_worker.id}/")
    assert response.status_code == 403
    assert response.json()["error"] == "Unauthorized"
