import json
from datetime import timedelta
from decimal import Decimal

import pytest
from app.models.order_models import Order
from django.utils import timezone
from datetime import timezone as dt_timezone


# ------------------------------------------------------------------
# GET /daily_stats - Stats endpoint for a restaurant
# ------------------------------------------------------------------

@pytest.mark.django_db
def test_daily_stats_unauthenticated(api_client):
    response = api_client.get("/daily_stats?date=2025-01-01")
    assert response.status_code == 401


@pytest.mark.django_db
def test_daily_stats_non_restaurant(api_client, custom_user):
    api_client.force_authenticate(user=custom_user)
    response = api_client.get("/daily_stats?date=2025-01-01")
    assert response.status_code == 403
    assert "Only restaurant accounts can access" in response.json()["error"]


@pytest.mark.django_db
def test_daily_stats_missing_date(api_client, restaurant):
    api_client.force_authenticate(user=restaurant.user)
    response = api_client.get("/daily_stats")
    assert response.status_code == 400
    assert response.json()["error"] == "Date is required"


@pytest.mark.django_db
def test_daily_stats_invalid_date_format(api_client, restaurant):
    api_client.force_authenticate(user=restaurant.user)
    response = api_client.get("/daily_stats?date=2025-13-40")
    assert response.status_code == 400
    assert response.json()["error"] == "Invalid date format"


@pytest.mark.django_db
def test_daily_stats_no_orders(api_client, restaurant):
    api_client.force_authenticate(user=restaurant.user)
    # Use today's date, but no orders exist
    date_str = timezone.now().date().isoformat()
    response = api_client.get(f"/daily_stats?date={date_str}")
    assert response.status_code == 200
    data = response.json()
    assert data == {
        "total_orders": 0,
        "total_sales": 0,
        "avg_order_value": 0,
        "active_workers": 0,
    }


@pytest.mark.django_db
def test_daily_stats_with_orders(api_client, restaurant, customer, worker):
    api_client.force_authenticate(user=restaurant.user)

    # Use fixed UTC time
    now = timezone.now().astimezone(dt_timezone.utc).replace(hour=12, minute=0, second=0, microsecond=0)
    date_str = now.date().isoformat()

    o1 = Order.objects.create(
        customer=customer,
        restaurant=restaurant,
        total_price=Decimal("15.50"),
        status="completed",
        worker=worker
    )
    o1.start_time = now - timedelta(hours=1)
    o1.save(update_fields=["start_time"])

    o2 = Order.objects.create(
        customer=customer,
        restaurant=restaurant,
        total_price=Decimal("10.00"),
        status="picked_up"
    )
    o2.start_time = now - timedelta(hours=2)
    o2.save(update_fields=["start_time"])

    response = api_client.get(f"/daily_stats?date={date_str}")
    assert response.status_code == 200
    data = response.json()
    print(data)

    assert data["total_orders"] == 2
    assert data["total_sales"] == 25.5
    assert data["avg_order_value"] == 12.75
    assert data["active_workers"] == 1


@pytest.mark.django_db
def test_daily_stats_invalid_method(api_client, restaurant):
    api_client.force_authenticate(user=restaurant.user)
    response = api_client.post("/daily_stats?date=2025-01-01", data=json.dumps({}), content_type="application/json")
    assert response.status_code == 405
    assert 'method "post" not allowed' in response.json().get("detail", "").lower()
