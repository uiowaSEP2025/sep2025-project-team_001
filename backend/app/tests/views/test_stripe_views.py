import json
from unittest.mock import patch

import pytest
from app.models.customer_models import CustomUser

# --- Fixtures ---

@pytest.fixture
def auth_client(api_client):
    """
    Returns an authenticated APIClient with a simple CustomUser.
    """
    user = CustomUser.objects.create_user(username="stripeuser", email="stripe@example.com", password="testpass")
    api_client.force_authenticate(user=user)
    return api_client


# --- create_payment_intent tests ---

@pytest.mark.django_db
@patch("app.mobileViews.stripeViews.stripe.PaymentIntent.create")
def test_create_payment_intent_success(mock_create, auth_client):
    mock_create.return_value.client_secret = "test_secret_123"
    data = {"amount": 5000}

    response = auth_client.post(
        "/order/payment/",
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == 200
    resp_data = response.json()
    assert resp_data["clientSecret"] == "test_secret_123"
    mock_create.assert_called_once_with(
        amount=5000,
        currency="usd",
        automatic_payment_methods={"enabled": True},
    )


@pytest.mark.django_db
@patch("app.mobileViews.stripeViews.stripe.PaymentIntent.create", side_effect=Exception("Stripe error"))
def test_create_payment_intent_failure(mock_create, auth_client):
    data = {"amount": 5000}
    response = auth_client.post(
        "/order/payment/",
        data=json.dumps(data),
        content_type="application/json",
    )
    assert response.status_code == 400
    assert "error" in response.json()


# --- create_setup_intent tests ---

@pytest.mark.django_db
@patch("app.mobileViews.stripeViews.stripe.SetupIntent.create")
def test_create_setup_intent_success(mock_create, auth_client):
    mock_create.return_value.client_secret = "setup_secret_abc"
    data = {"customer_id": "cus_123"}

    response = auth_client.post(
        "/order/setup/",
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == 200
    assert response.json()["clientSecret"] == "setup_secret_abc"
    mock_create.assert_called_once_with(
        customer="cus_123",
        payment_method_types=["card"],
    )


@pytest.mark.django_db
@patch("app.mobileViews.stripeViews.stripe.SetupIntent.create", side_effect=Exception("Invalid customer"))
def test_create_setup_intent_failure(mock_create, auth_client):
    data = {"customer_id": "invalid"}
    response = auth_client.post(
        "/order/setup/",
        data=json.dumps(data),
        content_type="application/json",
    )

    assert response.status_code == 400
    assert "error" in response.json()



# --- create_stripe_customer helper test ---

@patch("app.mobileViews.stripeViews.stripe.Customer.create")
def test_create_stripe_customer(mock_create):
    from app.mobileViews.stripeViews import create_stripe_customer

    mock_create.return_value.id = "cus_mocked_789"
    customer_id = create_stripe_customer("user@example.com")

    assert customer_id == "cus_mocked_789"
    mock_create.assert_called_once_with(email="user@example.com")
