import json
from unittest.mock import patch

import pytest

# ------------------------------------------------------------------
# POST /order/payment/ - Create a Stripe PaymentIntent
# ------------------------------------------------------------------

@pytest.mark.django_db
@patch("app.mobileViews.stripeViews.stripe.PaymentIntent.create")
def test_create_payment_intent_success(mock_create, auth_client):
    """
    A valid payment request should return 200 with clientSecret.
    """
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
    """
    If Stripe raises an error, should return 400 with error message.
    """
    data = {"amount": 5000}
    response = auth_client.post(
        "/order/payment/",
        data=json.dumps(data),
        content_type="application/json",
    )
    assert response.status_code == 400
    assert "error" in response.json()


# ------------------------------------------------------------------
# POST /order/setup/ - Create a Stripe SetupIntent
# ------------------------------------------------------------------

@pytest.mark.django_db
@patch("app.mobileViews.stripeViews.stripe.SetupIntent.create")
def test_create_setup_intent_success(mock_create, auth_client):
    """
    A valid setup request should return 200 with clientSecret.
    """
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
    """
    If Stripe raises an error, should return 400 with error message.
    """
    data = {"customer_id": "invalid"}
    response = auth_client.post(
        "/order/setup/",
        data=json.dumps(data),
        content_type="application/json",
    )
    assert response.status_code == 400
    assert "error" in response.json()


# ------------------------------------------------------------------
# Internal helper test - create_stripe_customer
# ------------------------------------------------------------------

@patch("app.mobileViews.stripeViews.stripe.Customer.create")
def test_create_stripe_customer(mock_create):
    """
    Verifies that create_stripe_customer helper returns the Stripe ID.
    """
    from app.mobileViews.stripeViews import create_stripe_customer

    mock_create.return_value.id = "cus_mocked_789"
    customer_id = create_stripe_customer("user@example.com")

    assert customer_id == "cus_mocked_789"
    mock_create.assert_called_once_with(email="user@example.com")
