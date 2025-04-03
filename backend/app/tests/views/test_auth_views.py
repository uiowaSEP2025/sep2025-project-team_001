import json

import pytest


@pytest.mark.django_db
def test_register_success(client):
    """
    Test that a valid registration creates a new user, manager, restaurant,
    and returns JWT tokens with expected information.
    """
    data = {
        "name": "John Doe",
        "username": "johndoe",
        "password": "strongpass",
        "email": "johndoe@example.com",
        "phone": "1234567890",
        "business_name": "John's Diner",
        "business_address": "123 Main St",
        "restaurantImage": "imagedata_that_is_longer_than_30_characters_for_truncation_test",
    }
    response = client.post(
        "/register/", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 201, response.content
    resp_data = response.json()
    assert resp_data.get("message") == "User registered successfully"
    # Check that tokens are returned.
    assert "tokens" in resp_data
    # Check Manager and Restaurant details.
    assert resp_data.get("manager") == "johndoe"
    assert resp_data.get("restaurant") == "John's Diner"
    expected_image = data["restaurantImage"][:30] + "..."
    assert resp_data.get("restaurant_image") == expected_image
    # Verify that the restaurant managers list includes the new user's username.
    assert "johndoe" in resp_data.get("restaurant_managers", [])


@pytest.mark.django_db
def test_register_missing_field(client):
    """
    Test that missing a required field (e.g. "name") returns a 400 error with an appropriate message.
    """
    data = {
        # "name" is missing
        "username": "janedoe",
        "password": "strongpass",
        "email": "janedoe@example.com",
        "phone": "1234567890",
        "business_name": "Jane's Cafe",
        "business_address": "456 Main St",
    }
    response = client.post(
        "/register/", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 400, response.content
    resp_data = response.json()
    assert "Name is required" in resp_data.get("message", "")


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
        "business_address": "123 Main St",
    }
    # First registration succeeds.
    client.post("/register/", data=json.dumps(data), content_type="application/json")
    # Second registration with the same username.
    data2 = {
        "name": "Jane Doe",
        "username": "johndoe",  # duplicate username
        "password": "strongpass",
        "email": "jane@example.com",
        "phone": "0987654321",
        "business_name": "Jane's Cafe",
        "business_address": "456 Main St",
    }
    response = client.post(
        "/register/", data=json.dumps(data2), content_type="application/json"
    )
    assert response.status_code == 400, response.content
    resp_data = response.json()
    assert "Username already taken" in resp_data.get("message", "")


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
        "email": "duplicate@example.com",  # duplicate email
        "phone": "0987654321",
        "business_name": "Jane's Cafe",
        "business_address": "456 Main St",
    }
    response = client.post(
        "/register/", data=json.dumps(data2), content_type="application/json"
    )
    assert response.status_code == 400, response.content
    resp_data = response.json()
    assert "Email already registered" in resp_data.get("message", "")


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
    response = client.post(
        "/register/", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 400, response.content
    resp_data = response.json()
    assert "Invalid email format" in resp_data.get("message", "")


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
    response = client.post(
        "/register/", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 400, response.content
    resp_data = response.json()
    assert "Phone number must be exactly 10 digits" in resp_data.get("message", "")


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
    response = client.post(
        "/register/", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 400, response.content
    resp_data = response.json()
    assert "Password must be at least 6 characters long" in resp_data.get("message", "")


# --- LOGIN TESTS ---


@pytest.mark.django_db
def test_login_success(client):
    """
    Test that a registered user can successfully login and receive JWT tokens,
    along with additional manager/restaurant info.
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
    client.post(
        "/register/", data=json.dumps(register_data), content_type="application/json"
    )

    # Now, attempt to login.
    login_data = {"username": "alice", "password": "strongpassword"}
    response = client.post(
        "/login/", data=json.dumps(login_data), content_type="application/json"
    )
    assert response.status_code == 200, response.content
    resp_data = response.json()
    assert "tokens" in resp_data
    assert resp_data.get("message") == "Login successful"
    assert resp_data.get("bar_name") is not None


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
    client.post(
        "/register/", data=json.dumps(register_data), content_type="application/json"
    )

    # Attempt to login with an incorrect password.
    login_data = {"username": "bob", "password": "wrongpassword"}
    response = client.post(
        "/login/", data=json.dumps(login_data), content_type="application/json"
    )
    assert response.status_code == 401, response.content
    resp_data = response.json()
    assert "Invalid credentials" in resp_data.get("error", "")


@pytest.mark.django_db
def test_login_invalid_method(client):
    """
    Test that a GET request to the login endpoint returns a 400 error.
    """
    response = client.get("/login/")
    assert response.status_code == 400, response.content
    resp_data = response.json()
    assert "Invalid request" in resp_data.get("error", "")
