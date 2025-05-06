import json

import pytest


# ------------------------------------------------------------------
# Stub out the real image uploader to avoid base64 padding errors
# ------------------------------------------------------------------
@pytest.fixture(autouse=True)
def patch_save_image(monkeypatch):
    monkeypatch.setattr(
        "app.views.auth_views.save_image_from_base64",
        lambda b64, folder, ref_id: f"http://test/{folder}/{ref_id}.png"
    )


# ------------------------------------------------------------------
# SHARED: Helper to generate registration data
# ------------------------------------------------------------------
def base_register_data(**overrides):
    data = {
        "name": "John Doe",
        "username": "johndoe",
        "password": "strongpass",
        "email": "johndoe@example.com",
        "phone": "1234567890",
        "business_name": "Testaurant",
        "business_address": "123 Main St",
        "restaurantImage": "not-even-valid-base64!!",
        "pin": "1234",
    }
    data.update(overrides)
    return data


# ------------------------------------------------------------------
# POST /register/ - User + restaurant registration
# ------------------------------------------------------------------
@pytest.mark.django_db
def test_register_success(client):
    data = base_register_data()
    resp = client.post(
        "/register/",
        data=json.dumps(data),
        content_type="application/json",
    )
    assert resp.status_code == 201
    js = resp.json()
    assert js["message"] == "User registered successfully"
    assert "tokens" in js


@pytest.mark.django_db
@pytest.mark.parametrize("field,expected_msg", [
    ("name", "Name is required."),
    ("username", "Username is required."),
    ("password", "Password is required."),
    ("email", "Email is required."),
    ("phone", "Phone is required."),
    ("business_name", "Business name is required."),
    ("business_address", "Business address is required."),
    ("restaurantImage", "Restaurantimage is required."),
    ("pin", "Pin is required."),
])
def test_register_missing_fields(client, field, expected_msg):
    data = base_register_data()
    del data[field]
    resp = client.post(
        "/register/",
        data=json.dumps(data),
        content_type="application/json",
    )
    assert resp.status_code == 400
    assert expected_msg in resp.json().get("message", "")


@pytest.mark.django_db
def test_register_duplicate_username(client):
    client.post("/register/", data=json.dumps(base_register_data()), content_type="application/json")
    # same username, new email
    dup = base_register_data(email="other@example.com")
    resp = client.post("/register/", data=json.dumps(dup), content_type="application/json")
    assert resp.status_code == 400
    assert "Username already taken" in resp.json().get("message", "")


@pytest.mark.django_db
def test_register_email_registered(client):
    client.post("/register/", data=json.dumps(base_register_data()), content_type="application/json")
    # same email, new username
    dup = base_register_data(username="newuser")
    resp = client.post("/register/", data=json.dumps(dup), content_type="application/json")
    assert resp.status_code == 400
    assert "Email already registered" in resp.json().get("message", "")


@pytest.mark.django_db
def test_register_invalid_email_format(client):
    resp = client.post(
        "/register/",
        data=json.dumps(base_register_data(email="bad-email")),
        content_type="application/json",
    )
    assert resp.status_code == 400
    assert "Invalid email format." in resp.json().get("message", "")


@pytest.mark.django_db
def test_register_invalid_phone(client):
    resp = client.post(
        "/register/",
        data=json.dumps(base_register_data(phone="12345")),
        content_type="application/json",
    )
    assert resp.status_code == 400
    assert "Phone number must be exactly 10 digits." in resp.json().get("message", "")


@pytest.mark.django_db
def test_register_short_password(client):
    resp = client.post(
        "/register/",
        data=json.dumps(base_register_data(password="123")),
        content_type="application/json",
    )
    assert resp.status_code == 400
    assert "Password must be at least 6 characters long." in resp.json().get("message", "")


def test_register_invalid_method(client):
    resp = client.get("/register/")
    assert resp.status_code == 400
    assert resp.json().get("error") == "Invalid request"


# ------------------------------------------------------------------
# POST /login_restaurant/ - Login via username/password
# ------------------------------------------------------------------
@pytest.mark.django_db
def test_login_restaurant_success(client):
    # first register
    client.post("/register/", data=json.dumps(base_register_data(username="mgr", email="mgr@example.com")),
                content_type="application/json")
    # then login
    creds = {"username": "mgr", "password": "strongpass"}
    resp = client.post("/login_restaurant/", data=json.dumps(creds), content_type="application/json")
    assert resp.status_code == 200
    js = resp.json()
    assert js["message"] == "Restaurant login successful"
    assert "tokens" in js
    assert js["bar_name"] == "Testaurant"


@pytest.mark.django_db
def test_login_restaurant_invalid_credentials(client):
    resp = client.post("/login_restaurant/", data=json.dumps({"username": "no", "password": "wrong"}),
                       content_type="application/json")
    assert resp.status_code == 401
    assert "Invalid username or password" in resp.json().get("error", "")


@pytest.mark.django_db
def test_login_restaurant_not_linked(client, custom_user):
    # user exists but no restaurant
    creds = {"username": custom_user.username, "password": "testpass"}
    resp = client.post("/login_restaurant/", data=json.dumps(creds), content_type="application/json")
    assert resp.status_code == 403
    assert "not linked to a restaurant" in resp.json().get("error", "")


def test_login_restaurant_invalid_method(client):
    resp = client.get("/login_restaurant/")
    assert resp.status_code == 400
    assert resp.json().get("error") == "Invalid request"


# ------------------------------------------------------------------
# POST /login_user/ - Login via Worker PIN
# ------------------------------------------------------------------
@pytest.mark.django_db
def test_login_user_success(client, manager_user_with_worker):
    info = manager_user_with_worker
    payload = {"pin": info["pin"], "restaurant_id": info["restaurant"].id}
    resp = client.post("/login_user/", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 200
    js = resp.json()
    assert js["message"] == "Worker login successful"
    assert js["role"] == "manager"


@pytest.mark.django_db
@pytest.mark.parametrize("payload,errmsg", [
    ({}, "PIN and restaurant_id are required."),
    ({"pin": "1234"}, "PIN and restaurant_id are required."),
    ({"restaurant_id": 1}, "PIN and restaurant_id are required."),
])
def test_login_user_missing_params(client, payload, errmsg):
    resp = client.post("/login_user/", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 400
    assert errmsg in resp.json().get("error", "")


@pytest.mark.django_db
def test_login_user_invalid_pin(client, manager_user_with_worker):
    info = manager_user_with_worker
    payload = {"pin": "wrongpin", "restaurant_id": info["restaurant"].id}
    resp = client.post("/login_user/", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 401
    assert "Invalid PIN for this restaurant." in resp.json().get("error", "")


def test_login_user_invalid_method(client):
    resp = client.get("/login_user/")
    assert resp.status_code == 400
    assert resp.json().get("error") == "Invalid request"
