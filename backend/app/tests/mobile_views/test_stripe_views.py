import json
from unittest.mock import patch

import pytest
import stripe
from app.models.customer_models import Customer, CustomUser
from rest_framework.test import APIClient


# ------------------------------------------------------------------
# Fixtures
# ------------------------------------------------------------------

@pytest.fixture
def api_client(db):
    return APIClient()


@pytest.fixture
def stripe_user(db):
    user = CustomUser.objects.create_user(
        username="stripeuser", email="stripe@example.com", password="testpass"
    )
    # attach a Customer record
    Customer.objects.create(user=user, stripe_customer_id="cus_test_123")
    return user


@pytest.fixture
def auth_client(api_client, stripe_user):
    api_client.force_authenticate(user=stripe_user)
    return api_client


# ------------------------------------------------------------------
# POST /order/payment/ - Create a Stripe PaymentIntent
# ------------------------------------------------------------------

@pytest.mark.django_db
@patch("app.mobileViews.stripeViews.stripe.PaymentIntent.create")
def test_create_payment_intent_success(mock_create, auth_client):
    """
    A valid payment request should return 200 with client_secret and customer_id.
    """
    mock_intent = mock_create.return_value
    mock_intent.client_secret = "test_secret_123"

    resp = auth_client.post(
        "/order/payment/",
        data=json.dumps({"amount": 5000}),
        content_type="application/json",
    )
    assert resp.status_code == 200, resp.content
    data = resp.json()
    assert data["client_secret"] == "test_secret_123"
    assert data["customer_id"] == "cus_test_123"
    mock_create.assert_called_once_with(
        amount=5000,
        currency="usd",
        customer="cus_test_123",
        automatic_payment_methods={"enabled": True},
    )


@pytest.mark.django_db
@patch("app.mobileViews.stripeViews.stripe.PaymentIntent.create", side_effect=Exception("Stripe error"))
def test_create_payment_intent_failure(mock_create, auth_client):
    """
    If Stripe throws, we get a 400 with an error field.
    """
    resp = auth_client.post(
        "/order/payment/",
        data=json.dumps({"amount": 5000}),
        content_type="application/json",
    )
    assert resp.status_code == 400
    assert "error" in resp.json()


# ------------------------------------------------------------------
# GET /order/payment/methods/ - List saved cards
# ------------------------------------------------------------------

@pytest.mark.django_db
@patch("app.mobileViews.stripeViews.stripe.PaymentMethod.list")
def test_list_saved_payment_methods_success(mock_list, auth_client):
    """
    Should return a JSON list of card summaries.
    """
    mock_pm = type("PM", (), {})()
    mock_pm.id = "pm_1"
    mock_pm.card = type("C", (), {
        "brand": "visa", "last4": "4242",
        "exp_month": 12, "exp_year": 2025
    })()
    mock_list.return_value = type("R", (), {"data": [mock_pm]})()

    resp = auth_client.get("/order/payment/methods/")
    assert resp.status_code == 200
    data = resp.json()
    assert "paymentMethods" in data
    assert data["paymentMethods"][0]["id"] == "pm_1"
    mock_list.assert_called_once_with(
        customer="cus_test_123",
        type="card"
    )


# ------------------------------------------------------------------
# POST /order/payment/saved_card/ - Charge a saved card
# ------------------------------------------------------------------

@pytest.mark.django_db
@patch("app.mobileViews.stripeViews.stripe.PaymentIntent.create")
def test_pay_with_saved_card_success(mock_create, auth_client):
    """
    off-session confirm should return JSON status.
    """
    intent = mock_create.return_value
    intent.status = "succeeded"

    resp = auth_client.post(
        "/order/payment/saved_card/",
        data=json.dumps({"amount": 2500, "payment_method_id": "pm_42"}),
        content_type="application/json",
    )
    assert resp.status_code == 200
    assert resp.json()["status"] == "succeeded"
    mock_create.assert_called_once_with(
        amount=2500,
        currency="usd",
        customer="cus_test_123",
        payment_method="pm_42",
        off_session=True,
        confirm=True,
    )


@pytest.mark.django_db
@patch("app.mobileViews.stripeViews.stripe.PaymentIntent.create", side_effect=stripe.error.CardError(
    message="Your card was declined",
    param=None, code=None, http_body=None, http_status=None, json_body=None, headers=None
))
def test_pay_with_saved_card_declined(mock_create, auth_client):
    """
    CardError should map to a 402 and include the user_message.
    """

    class Err(stripe.error.CardError):
        user_message = "Declined"

    mock_create.side_effect = Err(
        message="decline", param=None, code=None,
        http_body=None, http_status=None, json_body=None, headers=None
    )

    resp = auth_client.post(
        "/order/payment/saved_card/",
        data=json.dumps({"amount": 2500, "payment_method_id": "pm_bad"}),
        content_type="application/json",
    )
    assert resp.status_code == 402
    assert "error" in resp.json()


# ------------------------------------------------------------------
# DELETE /order/payment/saved_card/<id>/ - Detach a card
# ------------------------------------------------------------------

@pytest.mark.django_db
@patch("app.mobileViews.stripeViews.stripe.PaymentMethod.detach")
def test_delete_payment_method_success(mock_detach, auth_client):
    """
    Should return 200 + success message.
    """
    resp = auth_client.delete("/order/payment/saved_card/pm_99/")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Payment method detached successfully"
    mock_detach.assert_called_once_with("pm_99")


@pytest.mark.django_db
@patch("app.mobileViews.stripeViews.stripe.PaymentMethod.detach", side_effect=Exception("oops"))
def test_delete_payment_method_failure(mock_detach, auth_client):
    """
    Detach error should return 400 + error.
    """
    resp = auth_client.delete("/order/payment/saved_card/pm_99/")
    assert resp.status_code == 400
    assert "error" in resp.json()


# ------------------------------------------------------------------
# Internal helper test - create_stripe_customer
# ------------------------------------------------------------------

@patch("app.mobileViews.stripeViews.stripe.Customer.create")
def test_create_stripe_customer(mock_create):
    """
    Verifies that create_stripe_customer helper returns the Stripe ID.
    """
    from app.mobileViews.stripeViews import create_stripe_customer

    mock_create.return_value.id = "cus_xyz"
    cid = create_stripe_customer("me@here.com")
    assert cid == "cus_xyz"
    mock_create.assert_called_once_with(email="me@here.com")
