import pytest
from app.models.promotion_models import PromotionNotification
from django.utils import timezone


@pytest.mark.django_db
def test_promotion_defaults_and_str(restaurant_with_user):
    restaurant, _ = restaurant_with_user
    # Create a promotion without specifying sent or created_at
    before = timezone.now()
    promo = PromotionNotification.objects.create(
        restaurant=restaurant,
        title="Test Promo",
        body="Testing promotions"
    )
    after = timezone.now()

    # sent defaults to False
    assert promo.sent is False
    # created_at is set and within bounds
    assert before <= promo.created_at <= after
    # __str__ returns 'title - restaurant name'
    assert str(promo) == f"Test Promo - {restaurant.name}"
