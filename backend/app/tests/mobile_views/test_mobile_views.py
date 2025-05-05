import json

import pytest
from app.models.customer_models import Customer, CustomUser


# ------------------------------------------------------------------
# Helpers & fixtures
# ------------------------------------------------------------------

@pytest.fixture(autouse=True)
def patch_stripe(monkeypatch):
    # stub out the Stripe customer creation
    monkeypatch.setattr(
        "app.mobileViews.mobileViews.create_stripe_customer",
        lambda email: "cus_test_123"
    )


# ------------------------------------------------------------------
# POST /mobile/register/ - register_customer
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_mobile_register_success(api_client):
    payload = {
        "email": "new@example.com",
        "password": "securepass",
        "name": "Alice",
    }
    resp = api_client.post("/mobile/register/", data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 201, resp.content
    data = resp.json()
    assert data["message"] == "User registered successfully"
    assert data["stripe_customer_id"] == "cus_test_123"
    # make sure the user & customer exist
    user = CustomUser.objects.get(username="new@example.com")
    cust = Customer.objects.get(user=user)
    assert cust.stripe_customer_id == "cus_test_123"


@pytest.mark.django_db
def test_mobile_register_duplicate_email(api_client):
    # first registration
    api_client.post("/mobile/register/", data=json.dumps({
        "email": "dup@example.com", "password": "p", "name": "A"
    }), content_type="application/json")
    # try again
    resp = api_client.post("/mobile/register/", data=json.dumps({
        "email": "dup@example.com", "password": "x", "name": "B"
    }), content_type="application/json")
    assert resp.status_code == 400
    assert "Email already in use" in resp.json()["message"]


@pytest.mark.django_db
def test_mobile_register_invalid_method(api_client):
    resp = api_client.get("/mobile/register/")
    assert resp.status_code == 400
    assert resp.json()["error"] == "Invalid request"


# ------------------------------------------------------------------
# POST /mobile/login/ - login_customer
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_mobile_login_success(api_client):
    # first register
    api_client.post("/mobile/register/", json.dumps({
        "email": "log@example.com", "password": "pw", "name": "Z"
    }), content_type="application/json")
    # then login
    resp = api_client.post("/mobile/login/", data=json.dumps({
        "username": "log@example.com", "password": "pw"
    }), content_type="application/json")
    assert resp.status_code == 200, resp.content
    data = resp.json()
    assert data["message"] == "Login successful"
    assert "tokens" in data
    assert data["name"] == "Z"


@pytest.mark.django_db
def test_mobile_login_bad_credentials(api_client):
    # no such user
    resp = api_client.post("/mobile/login/", data=json.dumps({
        "username": "nouser", "password": "bad"
    }), content_type="application/json")
    assert resp.status_code == 401
    assert resp.json()["error"] == "Invalid credentials"


@pytest.mark.django_db
def test_mobile_login_invalid_method(api_client):
    resp = api_client.get("/mobile/login/")
    assert resp.status_code == 400
    assert resp.json()["error"] == "Invalid request"


@pytest.mark.django_db
def test_mobile_login_missing_fields(api_client):
    # missing password
    resp = api_client.post("/mobile/login/", data=json.dumps({
        "username": "someone"
    }), content_type="application/json")
    # authenticate will treat missing password as invalid
    assert resp.status_code == 401
    assert resp.json()["error"] == "Invalid credentials"
