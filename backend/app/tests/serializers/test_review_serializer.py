import pytest
from app.models.review_models import Review
from app.serializers.review_serializer import ReviewSerializer


@pytest.mark.django_db
def test_review_serializer_output(order_item, custom_user):
    """
    ReviewSerializer should correctly serialize a Review instance,
    including customer_name, worker_name (None), and items list.
    """
    order = order_item.order
    review = Review.objects.create(order=order, rating=4, comment="Great service")
    serializer = ReviewSerializer(review)
    data = serializer.data

    # Core fields
    assert data["id"] == review.id
    assert data["order"] == order.id
    assert data["rating"] == 4
    assert data["comment"] == "Great service"
    # created_at returned as ISO string
    assert isinstance(data["created_at"], str)

    # customer_name comes from order.customer.user.first_name
    assert data["customer_name"] == custom_user.first_name
    # worker_name should be None if no worker assigned
    assert data.get("worker_name") is None

    # items list contains the item names from order_items
    assert data["items"] == [order_item.item.name]


@pytest.mark.django_db
def test_review_serializer_deserialization_valid(order):
    """
    Valid input data should deserialize and create a Review instance.
    """
    payload = {
        "order": order.id,
        "rating": 5,
        "comment": "Excellent!"
    }
    serializer = ReviewSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors
    review = serializer.save()

    assert review.order == order
    assert review.rating == 5
    assert review.comment == "Excellent!"


@pytest.mark.django_db
def test_review_serializer_default_rating_and_blank_comment(order):
    """
    Omitting rating should default to 5; comment defaults to blank.
    """
    payload = {"order": order.id}
    serializer = ReviewSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors
    review = serializer.save()

    assert review.rating == 5
    assert review.comment == ""


@pytest.mark.django_db
def test_review_serializer_invalid_negative_rating(order):
    """
    Negative rating should fail validation (PositiveIntegerField).
    """
    payload = {"order": order.id, "rating": -1}
    serializer = ReviewSerializer(data=payload)
    assert not serializer.is_valid()
    assert "rating" in serializer.errors


@pytest.mark.django_db
def test_review_serializer_invalid_non_integer_rating(order):
    """
    Non-integer rating should fail validation.
    """
    payload = {"order": order.id, "rating": "bad"}
    serializer = ReviewSerializer(data=payload)
    assert not serializer.is_valid()
    assert "rating" in serializer.errors


@pytest.mark.django_db
def test_review_serializer_extra_unexpected_fields_ignored(order):
    """
    Passing unexpected fields should be ignored, not error.
    """
    payload = {"order": order.id, "rating": 3, "foo": "bar"}
    serializer = ReviewSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors
    # 'foo' should not appear in validated_data
    assert "foo" not in serializer.validated_data
