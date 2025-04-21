import json
from unittest.mock import patch

import pytest
from app.models import Customer, CustomUser


# ------------------------------------------------------------------
# POST /mobile/register/ - Register a mobile customer
# ------------------------------------------------------------------

@pytest.mark.django_db
@patch("app.mobileViews.mobileViews.create_stripe_customer", return_value="cus_mocked_123")
def test_register_customer_success(mock_stripe, api_client):
    """
    A valid registration should create a user, customer, and return Stripe customer ID.
    """
    data = {
        "email": "mobile@example.com",
        "password": "mobilepass",
        "name": "Mobile User",
    }
    response = api_client.post("/mobile/register/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 201, response.content
    resp_data = response.json()
    assert resp_data.get("message") == "User registered successfully"
    assert "tokens" in resp_data
    assert resp_data["stripe_customer_id"] == "cus_mocked_123"

    user = CustomUser.objects.get(username="mobile@example.com")
    customer = Customer.objects.get(user=user)
    assert customer is not None


@pytest.mark.django_db
@patch("app.mobileViews.mobileViews.create_stripe_customer", return_value="cus_mocked_123")
def test_register_customer_duplicate_email(mock_stripe, api_client):
    """
    Registering a user with an existing email should return 400.
    """
    data = {
        "email": "duplicate@example.com",
        "password": "pass123",
        "name": "First User",
    }
    api_client.post("/mobile/register/", data=json.dumps(data), content_type="application/json")

    data2 = {
        "email": "duplicate@example.com",
        "password": "pass456",
        "name": "Second User",
    }
    response = api_client.post("/mobile/register/", data=json.dumps(data2), content_type="application/json")
    assert response.status_code == 400
    assert "Email already in use" in response.json().get("message", "")


@pytest.mark.django_db
def test_register_customer_missing_fields(api_client):
    """
    Registration missing a required field should return 500 (handled inside try/except).
    """
    response = api_client.post("/mobile/register/", data=json.dumps({"email": "missing@example.com"}), content_type="application/json")
    assert response.status_code == 500
    assert "error" in response.json()


def test_register_customer_invalid_json(api_client):
    """
    Invalid JSON payload should return 400 or 500 depending on handling.
    """
    response = api_client.post("/mobile/register/", data="not-json", content_type="application/json")
    assert response.status_code in [400, 500]


@pytest.mark.django_db
def test_register_customer_invalid_method(api_client):
    """
    GET request to /mobile/register/ should return 400.
    """
    response = api_client.get("/mobile/register/")
    assert response.status_code == 400
    assert "Invalid request" in response.json().get("error", "")


# ------------------------------------------------------------------
# POST /mobile/login/ - Authenticate a mobile customer
# ------------------------------------------------------------------

@pytest.mark.django_db
@patch("app.mobileViews.mobileViews.create_stripe_customer", return_value="cus_mocked_123")
def test_login_customer_success(mock_stripe, api_client):
    """
    A valid email/password login should return JWT tokens and customer info.
    """
    reg_data = {
        "email": "login@example.com",
        "password": "loginpass",
        "name": "Login User",
    }
    reg_response = api_client.post("/mobile/register/", data=json.dumps(reg_data), content_type="application/json")
    assert reg_response.status_code == 201

    login_data = {
        "username": "login@example.com",
        "password": "loginpass",
    }
    response = api_client.post("/mobile/login/", data=json.dumps(login_data), content_type="application/json")
    assert response.status_code == 200
    resp_data = response.json()
    assert resp_data.get("message") == "Login successful"
    assert "tokens" in resp_data
    assert resp_data.get("name") == "Login User"


@pytest.mark.django_db
@patch("app.mobileViews.mobileViews.create_stripe_customer", return_value="cus_mocked_123")
def test_login_customer_invalid_credentials(mock_stripe, api_client):
    """
    Logging in with an incorrect password should return 401 Unauthorized.
    """
    reg_data = {
        "email": "wronglogin@example.com",
        "password": "correctpass",
        "name": "Wrong Login User",
    }
    api_client.post("/mobile/register/", data=json.dumps(reg_data), content_type="application/json")

    login_data = {
        "username": "wronglogin@example.com",
        "password": "wrongpass",
    }
    response = api_client.post("/mobile/login/", data=json.dumps(login_data), content_type="application/json")
    assert response.status_code == 401
    assert "Invalid credentials" in response.json().get("error", "")


@pytest.mark.django_db
def test_login_customer_nonexistent_user(api_client):
    """
    Logging in with an email that doesn't exist should return 401.
    """
    login_data = {"username": "nonexistent@example.com", "password": "anything"}
    response = api_client.post("/mobile/login/", data=json.dumps(login_data), content_type="application/json")
    assert response.status_code == 401
    assert "Invalid credentials" in response.json().get("error", "")


@pytest.mark.django_db
def test_login_customer_invalid_method(api_client):
    """
    GET request to /mobile/login/ should return 400.
    """
    response = api_client.get("/mobile/login/")
    assert response.status_code == 400
    assert "Invalid request" in response.json().get("error", "")
