import pytest
from app.models.promotion_models import PromotionNotification as PromoModel
from app.serializers.promotion_serializer import PromotionNotificationSerializer
from rest_framework.exceptions import ValidationError


@pytest.mark.django_db
def test_promotion_serializer_serializes_all_fields(restaurant_with_user):
    restaurant, _ = restaurant_with_user
    promo = PromoModel.objects.create(
        restaurant=restaurant,
        title="Serialize Promo",
        body="Check serialization",
        sent=True
    )
    serializer = PromotionNotificationSerializer(instance=promo)
    data = serializer.data

    # All model fields should appear in serialized data
    expected_keys = {"id", "restaurant", "title", "body", "created_at", "sent"}
    assert set(data.keys()) == expected_keys
    # Values match
    assert data["restaurant"] == restaurant.id
    assert data["title"] == "Serialize Promo"
    assert data["body"] == "Check serialization"
    assert data["sent"] is True


@pytest.mark.django_db
def test_promotion_serializer_validation_errors():
    # Missing required fields should raise ValidationError
    serializer = PromotionNotificationSerializer(data={})
    with pytest.raises(ValidationError) as excinfo:
        serializer.is_valid(raise_exception=True)
    errors = excinfo.value.detail
    # Both title and body (and restaurant) are required
    assert "title" in errors
    assert "body" in errors
    assert "restaurant" in errors
