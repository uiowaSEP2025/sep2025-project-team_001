import json

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient

User = get_user_model()


@pytest.fixture
def api_client():
    return APIClient()


@pytest.mark.django_db
def test_register_customer_success(api_client):
    """
    Test that a valid POST request to /mobile/register/ creates a new user,
    a corresponding Customer, and returns JWT tokens.
    """
    data = {
        "email": "mobile@example.com",
        "password": "mobilepass",
        "name": "Mobile User"
    }
    response = api_client.post("/mobile/register/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 201, response.content
    resp_data = response.json()
    assert resp_data.get("message") == "User registered successfully"
    assert "tokens" in resp_data

    # Verify that the user was created.
    user = User.objects.get(username="mobile@example.com")
    assert user.email == "mobile@example.com"
    # Verify that a corresponding Customer exists.
    from app.models.customer_models import Customer
    customer = Customer.objects.get(user=user)
    assert customer is not None


@pytest.mark.django_db
def test_register_customer_duplicate_email(api_client):
    """
    Test that attempting to register with an already used email returns an error.
    """
    data = {
        "email": "duplicate@example.com",
        "password": "pass123",
        "name": "First User"
    }
    # First registration.
    response1 = api_client.post("/mobile/register/", data=json.dumps(data), content_type="application/json")
    assert response1.status_code == 201

    # Second registration with the same email.
    data2 = {
        "email": "duplicate@example.com",
        "password": "pass456",
        "name": "Second User"
    }
    response2 = api_client.post("/mobile/register/", data=json.dumps(data2), content_type="application/json")
    assert response2.status_code == 400
    resp_data = response2.json()
    assert "Email already in use" in resp_data.get("message", "")


@pytest.mark.django_db
def test_register_customer_invalid_method(api_client):
    """
    Test that a GET request to /mobile/register/ returns a 400 error.
    """
    response = api_client.get("/mobile/register/")
    assert response.status_code == 400
    resp_data = response.json()
    assert "Invalid request" in resp_data.get("error", "")


@pytest.mark.django_db
def test_login_customer_success(api_client):
    """
    Test that a registered customer can log in successfully.
    """
    # Register a user first.
    reg_data = {
        "email": "login@example.com",
        "password": "loginpass",
        "name": "Login User"
    }
    reg_response = api_client.post("/mobile/register/", data=json.dumps(reg_data), content_type="application/json")
    assert reg_response.status_code == 201

    # Now, log in with the correct credentials.
    login_data = {
        "username": "login@example.com",  # The mobile registration uses email as username.
        "password": "loginpass"
    }
    login_response = api_client.post("/mobile/login/", data=json.dumps(login_data), content_type="application/json")
    assert login_response.status_code == 200, login_response.content
    resp_data = login_response.json()
    assert resp_data.get("message") == "Login successful"
    assert "tokens" in resp_data


@pytest.mark.django_db
def test_login_customer_invalid_credentials(api_client):
    """
    Test that login with incorrect credentials returns a 401 error.
    """
    # Register a user.
    reg_data = {
        "email": "wronglogin@example.com",
        "password": "correctpass",
        "name": "Wrong Login User"
    }
    reg_response = api_client.post("/mobile/register/", data=json.dumps(reg_data), content_type="application/json")
    assert reg_response.status_code == 201

    # Attempt login with an incorrect password.
    login_data = {
        "username": "wronglogin@example.com",
        "password": "wrongpass"
    }
    login_response = api_client.post("/mobile/login/", data=json.dumps(login_data), content_type="application/json")
    assert login_response.status_code == 401, login_response.content
    resp_data = login_response.json()
    assert "Invalid credentials" in resp_data.get("error", "")


@pytest.mark.django_db
def test_login_customer_invalid_method(api_client):
    """
    Test that a GET request to /mobile/login/ returns a 400 error.
    """
    response = api_client.get("/mobile/login/")
    assert response.status_code == 400
    resp_data = response.json()
    assert "Invalid request" in resp_data.get("error", "")
