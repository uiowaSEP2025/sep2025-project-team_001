import json

import pytest

# --- SHARED REGISTER PAYLOAD ---

def base_register_data(**overrides):
    data = {
        "name": "John Doe",
        "username": "johndoe",
        "password": "strongpass",
        "email": "johndoe@example.com",
        "phone": "1234567890",
        "business_name": "John's Diner",
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
    assert response.status_code == 201, response.content
    resp_data = response.json()
    assert resp_data.get("message") == "User registered successfully"
    assert "tokens" in resp_data
    assert resp_data.get("restaurant") == data["business_name"]
    assert resp_data.get("restaurant_id") is not None


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
    register_data = base_register_data(username="alice", email="alice@example.com")
    client.post("/register/", data=json.dumps(register_data), content_type="application/json")

    login_data = {
        "username": "alice",
        "password": "strongpass"
    }
    response = client.post("/login/", data=json.dumps(login_data), content_type="application/json")
    assert response.status_code == 200
    resp_data = response.json()
    assert "tokens" in resp_data
    assert resp_data.get("message") == "Login successful"
    assert resp_data.get("bar_name") == register_data["business_name"]


@pytest.mark.django_db
def test_login_invalid_credentials(client):
    register_data = base_register_data(username="bob", email="bob@example.com")
    client.post("/register/", data=json.dumps(register_data), content_type="application/json")

    login_data = {
        "username": "bob",
        "password": "wrongpass"
    }
    response = client.post("/login/", data=json.dumps(login_data), content_type="application/json")
    assert response.status_code == 401
    assert "Invalid credentials" in response.json().get("error", "")


@pytest.mark.django_db
def test_login_invalid_method(client):
    response = client.get("/login/")
    assert response.status_code == 400
    assert "Invalid request" in response.json().get("error", "")
