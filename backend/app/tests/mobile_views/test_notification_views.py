import json

import pytest
from rest_framework import status


# No need to reverse() here since we're using the literal path from your urls.py:
URL = "/mobile/fcm_token/"


@pytest.mark.django_db
def test_save_fcm_token_unauthenticated(api_client, customer):
    """
    Unauthenticated POST to save_fcm_token should return 401.
    """
    payload = {"customer_id": customer.id, "fcm_token": "token123"}
    resp = api_client.post(URL, data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED


@pytest.mark.django_db
def test_save_fcm_token_success(api_client, customer):
    """
    Authenticated POST with a valid customer_id should save the token.
    """
    # Authenticate as the linked user
    api_client.force_authenticate(user=customer.user)

    payload = {"customer_id": customer.id, "fcm_token": "token123"}
    resp = api_client.post(URL, data=json.dumps(payload), content_type="application/json")

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json() == {"message": "Token saved successfully"}

    # Confirm it was persisted
    customer.refresh_from_db()
    assert customer.fcm_token == "token123"


@pytest.mark.django_db
def test_save_fcm_token_invalid_customer(api_client, customer):
    """
    Authenticated POST with a non-existent customer_id should return 500.
    """
    api_client.force_authenticate(user=customer.user)

    payload = {"customer_id": 9999, "fcm_token": "token123"}
    resp = api_client.post(URL, data=json.dumps(payload), content_type="application/json")
    assert resp.status_code == 404
    assert "error" in resp.json()
    assert "not found" in resp.json()["error"].lower()
