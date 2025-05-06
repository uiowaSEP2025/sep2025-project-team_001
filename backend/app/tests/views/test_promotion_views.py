# app/tests/views/test_promotion_views.py
import json
import time

import pytest
from app.models.customer_models import Customer, CustomUser
from app.models.promotion_models import PromotionNotification
from app.models.restaurant_models import Restaurant


@pytest.mark.django_db
def test_list_promotions_empty(api_client, restaurant_with_user):
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)

    resp = api_client.get("/promotions/")
    assert resp.status_code == 200
    assert resp.json() == []


@pytest.mark.django_db
def test_list_promotions_filters_by_restaurant(api_client, restaurant_with_user):
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    # Create promotions for this restaurant
    p1 = PromotionNotification.objects.create(
        restaurant=restaurant, title="Old Promo", body="Desc1"
    )
    time.sleep(5)  # Ensure different timestamps
    p2 = PromotionNotification.objects.create(
        restaurant=restaurant, title="New Promo", body="Desc2"
    )
    # Create promotion for another restaurant with its own user
    other_user = CustomUser.objects.create_user(
        username="other", email="other@example.com", password="pw"
    )
    other_rest = Restaurant.objects.create(
        user=other_user, name="Other"
    )
    PromotionNotification.objects.create(
        restaurant=other_rest, title="Other Promo", body="Desc3"
    )

    resp = api_client.get("/promotions/")
    assert resp.status_code == 200
    data = resp.json()
    # Should be ordered by created_at descending
    assert [d["id"] for d in data] == [p2.id, p1.id]


@pytest.mark.django_db
def test_create_promotion_success(api_client, restaurant_with_user):
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)

    payload = {"title": "Sale", "body": "Big sale today!"}
    resp = api_client.post(
        "/promotions/create/",
        data=json.dumps(payload),
        content_type="application/json",
    )
    assert resp.status_code == 201
    result = resp.json()
    # Verify fields
    assert result["title"] == "Sale"
    assert result["body"] == "Big sale today!"
    assert result["restaurant"] == restaurant.id
    assert result["sent"] is False


@pytest.mark.django_db
def test_create_promotion_invalid(api_client, restaurant_with_user):
    _, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    resp = api_client.post(
        "/promotions/create/",
        data=json.dumps({}),
        content_type="application/json",
    )
    assert resp.status_code == 400
    errors = resp.json()
    assert "title" in errors
    assert "body" in errors


@pytest.mark.django_db
def test_update_promotion_success(api_client, restaurant_with_user):
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    promo = PromotionNotification.objects.create(
        restaurant=restaurant, title="Old", body="Body"
    )

    resp = api_client.patch(
        f"/promotions/{promo.id}/update/",
        data=json.dumps({"title": "Updated"}),
        content_type="application/json",
    )
    assert resp.status_code == 200
    result = resp.json()
    assert result["id"] == promo.id
    assert result["title"] == "Updated"


@pytest.mark.django_db
def test_update_promotion_not_found(api_client, restaurant_with_user):
    _, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    resp = api_client.patch(
        "/promotions/999/update/",
        data=json.dumps({}),
        content_type="application/json",
    )
    assert resp.status_code == 404
    assert resp.json()["error"] == "Promotion not found"


@pytest.mark.django_db
def test_delete_promotion_success(api_client, restaurant_with_user):
    restaurant, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    promo = PromotionNotification.objects.create(
        restaurant=restaurant, title="X", body="Y"
    )

    resp = api_client.delete(f"/promotions/{promo.id}/delete/")
    assert resp.status_code == 204
    assert not PromotionNotification.objects.filter(id=promo.id).exists()


@pytest.mark.django_db
def test_delete_promotion_not_found(api_client, restaurant_with_user):
    _, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    resp = api_client.delete(
        "/promotions/999/delete/"
    )
    assert resp.status_code == 404
    assert resp.json()["error"] == "Promotion not found"


@pytest.mark.django_db
def test_send_promotion_success(api_client, restaurant_with_user, customer, monkeypatch):
    restaurant, user = restaurant_with_user
    # Prepare customers with tokens
    customer.fcm_token = "token1"
    customer.save()
    new_user = CustomUser.objects.create_user(
        username="c2", email="c2@test.com", password="pw"
    )
    Customer.objects.create(
        user=new_user, fcm_token="token2"
    )
    promo = PromotionNotification.objects.create(
        restaurant=restaurant, title="Flash", body="Hurry up!"
    )

    calls = []
    monkeypatch.setattr(
        "app.views.promotion_views.send_notification_to_device",
        lambda device_token, title, body, data: calls.append((device_token, title, body, data))
    )

    api_client.force_authenticate(user=user)
    resp = api_client.post(f"/promotions/{promo.id}/send/")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Promotion sent!"
    promo.refresh_from_db()
    assert promo.sent is True
    # Two customers with tokens
    assert len(calls) == 2


@pytest.mark.django_db
def test_send_promotion_not_found(api_client, restaurant_with_user):
    _, user = restaurant_with_user
    api_client.force_authenticate(user=user)
    resp = api_client.post("/promotions/999/send/")
    assert resp.status_code == 404
    assert resp.json()["error"] == "Promotion not found"
