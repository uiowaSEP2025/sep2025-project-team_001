import json

import pytest
from app.models import CustomUser

# --- SHARED REGISTER PAYLOAD ---

def base_register_data(**overrides):
    data = {
        "name": "John Doe",
        "username": "johndoe",
        "password": "strongpass",
        "email": "johndoe@example.com",
        "phone": "1234567890",
        "business_name": "Testaurant",
        "business_address": "123 Main St",
        "restaurantImage": "imagedata_that_is_longer_than_30_characters_for_truncation_test",
        "pin": "1234"
    }
    data.update(overrides)
    return data


# --- REGISTER TESTS ---

@pytest.mark.django_db
def test_register_success(client):
    data = base_register_data()
    response = client.post("/register/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 201
    resp = response.json()
    assert "tokens" in resp
    assert resp["message"] == "User registered successfully"


@pytest.mark.django_db
def test_register_missing_field(client):
    data = base_register_data()
    del data["name"]
    response = client.post("/register/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert "Name is required" in response.json().get("message", "")


@pytest.mark.django_db
def test_register_username_taken(client):
    data = base_register_data()
    client.post("/register/", data=json.dumps(data), content_type="application/json")

    data2 = base_register_data(
        name="Another",
        email="another@example.com"
    )
    response = client.post("/register/", data=json.dumps(data2), content_type="application/json")
    assert response.status_code == 400
    assert "Username already taken" in response.json().get("message", "")


@pytest.mark.django_db
def test_register_email_registered(client):
    data = base_register_data()
    client.post("/register/", data=json.dumps(data), content_type="application/json")

    data2 = base_register_data(
        username="newuser"
    )
    response = client.post("/register/", data=json.dumps(data2), content_type="application/json")
    assert response.status_code == 400
    assert "Email already registered" in response.json().get("message", "")


@pytest.mark.django_db
def test_register_invalid_email(client):
    data = base_register_data(email="not-an-email")
    response = client.post("/register/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert "Invalid email format" in response.json().get("message", "")


@pytest.mark.django_db
def test_register_invalid_phone(client):
    data = base_register_data(phone="12345")
    response = client.post("/register/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert "Phone number must be exactly 10 digits" in response.json().get("message", "")


@pytest.mark.django_db
def test_register_short_password(client):
    data = base_register_data(password="123")
    response = client.post("/register/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    assert "Password must be at least 6 characters long" in response.json().get("message", "")


# --- LOGIN TESTS ---

@pytest.mark.django_db
def test_login_success(client):
    data = base_register_data(username="loginuser", email="login@example.com")
    client.post("/register/", data=json.dumps(data), content_type="application/json")

    login_data = {"username": "loginuser", "password": "strongpass"}
    response = client.post("/login/", data=json.dumps(login_data), content_type="application/json")
    assert response.status_code == 200
    assert "tokens" in response.json()
    assert response.json()["bar_name"] == "Testaurant"


@pytest.mark.django_db
def test_login_with_pin_success(api_client, manager_user_with_worker):
    pin = manager_user_with_worker["pin"]
    response = api_client.post(
        "/login/", data=json.dumps({"pin": pin}), content_type="application/json"
    )
    assert response.status_code == 200
    data = response.json()
    assert data["role"] == "manager"
    assert data["bar_name"] == manager_user_with_worker["restaurant"].name


@pytest.mark.django_db
def test_login_with_invalid_pin(client):
    login_data = {"pin": "wrongpin"}
    response = client.post("/login/", data=json.dumps(login_data), content_type="application/json")
    assert response.status_code == 401
    assert response.json()["error"] == "Invalid pin"


@pytest.mark.django_db
def test_login_invalid_credentials(client):
    data = base_register_data(username="bob", email="bob@example.com")
    client.post("/register/", data=json.dumps(data), content_type="application/json")

    login_data = {"username": "bob", "password": "wrongpass"}
    response = client.post("/login/", data=json.dumps(login_data), content_type="application/json")
    assert response.status_code == 401
    assert "Invalid credentials" in response.json().get("error", "")


@pytest.mark.django_db
def test_login_user_without_restaurant(client, user):
    login_data = {"username": user.username, "password": "testpass"}
    response = client.post("/login/", data=json.dumps(login_data), content_type="application/json")
    assert response.status_code == 403
    assert "not linked to a restaurant" in response.json()["error"]


@pytest.mark.django_db
def test_login_invalid_method(client):
    response = client.get("/login/")
    assert response.status_code == 400
    assert "Invalid request" in response.json().get("error", "")
