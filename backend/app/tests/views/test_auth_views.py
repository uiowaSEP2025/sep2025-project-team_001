import json

import pytest
from django.contrib.auth import get_user_model

User = get_user_model()


@pytest.mark.django_db
def test_register_success(client):
    """
    Test that a valid registration creates a new user, manager, restaurant, and returns JWT tokens.
    """
    data = {
        "name": "John Doe",
        "username": "johndoe",
        "password": "strongpass",
        "email": "johndoe@example.com",
        "phone": "1234567890",
        "business_name": "John's Diner",
        "business_address": "123 Main St",
        "restaurantImage": "imagedata_that_is_longer_than_30_characters_for_truncation_test"
    }
    response = client.post(
        "/register/",
        data=json.dumps(data),
        content_type="application/json"
    )
    assert response.status_code == 201, response.content
    response_data = json.loads(response.content)
    assert response_data["message"] == "User registered successfully"
    # Check tokens are returned.
    assert "tokens" in response_data
    # Check manager and restaurant details.
    assert response_data["manager"] == "johndoe"
    assert response_data["restaurant"] == "John's Diner"
    # Check restaurant_image is truncated.
    expected_image = data["restaurantImage"][:30] + "..."
    assert response_data["restaurant_image"] == expected_image
    # Check that the restaurant_managers list includes the new user's username.
    assert "johndoe" in response_data["restaurant_managers"]


@pytest.mark.django_db
def test_register_missing_field(client):
    """
    Test that missing a required field (e.g., "name") returns a 400 error with an appropriate message.
    """
    data = {
        # "name" is missing
        "username": "janedoe",
        "password": "strongpass",
        "email": "janedoe@example.com",
        "phone": "1234567890",
        "business_name": "Jane's Cafe",
        "business_address": "456 Main St"
    }
    response = client.post(
        "/register/",
        data=json.dumps(data),
        content_type="application/json"
    )
    assert response.status_code == 400
    response_data = json.loads(response.content)
    assert "Name is required" in response_data["message"]


@pytest.mark.django_db
def test_register_username_taken(client):
    """
    Test that attempting to register with an already-taken username returns a 400 error.
    """
    data = {
        "name": "John Doe",
        "username": "johndoe",
        "password": "strongpass",
        "email": "john1@example.com",
        "phone": "1234567890",
        "business_name": "John's Diner",
        "business_address": "123 Main St"
    }
    # First registration succeeds.
    client.post("/register/", data=json.dumps(data), content_type="application/json")
    # Second registration with the same username.
    data2 = {
        "name": "Jane Doe",
        "username": "johndoe",  # same username
        "password": "strongpass",
        "email": "jane@example.com",
        "phone": "0987654321",
        "business_name": "Jane's Cafe",
        "business_address": "456 Main St",
    }
    response = client.post("/register/", data=json.dumps(data2), content_type="application/json")
    assert response.status_code == 400
    response_data = json.loads(response.content)
    assert "Username already taken" in response_data["message"]


@pytest.mark.django_db
def test_register_email_registered(client):
    """
    Test that attempting to register with an already-registered email returns a 400 error.
    """
    data = {
        "name": "John Doe",
        "username": "john1",
        "password": "strongpass",
        "email": "duplicate@example.com",
        "phone": "1234567890",
        "business_name": "John's Diner",
        "business_address": "123 Main St",
    }
    client.post("/register/", data=json.dumps(data), content_type="application/json")
    data2 = {
        "name": "Jane Doe",
        "username": "jane1",
        "password": "strongpass",
        "email": "duplicate@example.com",  # same email
        "phone": "0987654321",
        "business_name": "Jane's Cafe",
        "business_address": "456 Main St",
    }
    response = client.post("/register/", data=json.dumps(data2), content_type="application/json")
    assert response.status_code == 400
    response_data = json.loads(response.content)
    assert "Email already registered" in response_data["message"]


@pytest.mark.django_db
def test_register_invalid_email(client):
    """
    Test that an invalid email format returns a 400 error.
    """
    data = {
        "name": "John Doe",
        "username": "johndoe2",
        "password": "strongpass",
        "email": "not-an-email",
        "phone": "1234567890",
        "business_name": "John's Diner",
        "business_address": "123 Main St",
    }
    response = client.post("/register/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    response_data = json.loads(response.content)
    assert "Invalid email format" in response_data["message"]


@pytest.mark.django_db
def test_register_invalid_phone(client):
    """
    Test that an invalid phone number (not exactly 10 digits) returns a 400 error.
    """
    data = {
        "name": "John Doe",
        "username": "johndoe3",
        "password": "strongpass",
        "email": "john3@example.com",
        "phone": "12345",  # invalid phone
        "business_name": "John's Diner",
        "business_address": "123 Main St",
    }
    response = client.post("/register/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    response_data = json.loads(response.content)
    assert "Phone number must be exactly 10 digits" in response_data["message"]


@pytest.mark.django_db
def test_register_short_password(client):
    """
    Test that a password shorter than 6 characters returns a 400 error.
    """
    data = {
        "name": "John Doe",
        "username": "johndoe4",
        "password": "123",  # too short
        "email": "john4@example.com",
        "phone": "1234567890",
        "business_name": "John's Diner",
        "business_address": "123 Main St",
    }
    response = client.post("/register/", data=json.dumps(data), content_type="application/json")
    assert response.status_code == 400
    response_data = json.loads(response.content)
    assert "Password must be at least 6 characters long" in response_data["message"]


# --- LOGIN TESTS ---

@pytest.mark.django_db
def test_login_success(client):
    """
    Test that a registered user can successfully login and receive JWT tokens.
    """
    # First, register a user.
    register_data = {
        "name": "Alice",
        "username": "alice",
        "password": "strongpassword",
        "email": "alice@example.com",
        "phone": "1112223333",
        "business_name": "Alice's Restaurant",
        "business_address": "789 Main St",
    }
    client.post("/register/", data=json.dumps(register_data), content_type="application/json")

    # Now, attempt to login with correct credentials.
    login_data = {
        "username": "alice",
        "password": "strongpassword"
    }
    response = client.post("/login/", data=json.dumps(login_data), content_type="application/json")
    assert response.status_code == 200, response.content
    response_data = json.loads(response.content)
    assert "tokens" in response_data
    assert response_data["message"] == "Login successful"


@pytest.mark.django_db
def test_login_invalid_credentials(client):
    """
    Test that login fails with invalid credentials.
    """
    # Register a user.
    register_data = {
        "name": "Bob",
        "username": "bob",
        "password": "securepass",
        "email": "bob@example.com",
        "phone": "4445556666",
        "business_name": "Bob's Burgers",
        "business_address": "101 Main St",
    }
    client.post("/register/", data=json.dumps(register_data), content_type="application/json")

    # Attempt to login with a wrong password.
    login_data = {
        "username": "bob",
        "password": "wrongpassword"
    }
    response = client.post("/login/", data=json.dumps(login_data), content_type="application/json")
    assert response.status_code == 401
    response_data = json.loads(response.content)
    assert "Invalid credentials" in response_data["error"]


@pytest.mark.django_db
def test_login_invalid_method(client):
    """
    Test that a GET request to the login endpoint returns an error.
    """
    response = client.get("/login/")
    assert response.status_code == 400
    response_data = json.loads(response.content)
    assert "Invalid request" in response_data["error"]
