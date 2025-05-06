# app/tests/models/test_review_model.py

from datetime import datetime

import pytest
from app.models.review_models import Review
from django.core.exceptions import ValidationError
from django.db import IntegrityError


@pytest.mark.django_db
def test_default_review_fields(order):
    """
    A fresh Review should default to rating=5, empty comment,
    and have a datetime in created_at.
    """
    review = Review.objects.create(order=order)
    assert review.rating == 5
    assert review.comment == ""
    assert isinstance(review.created_at, datetime)


@pytest.mark.django_db
def test_str_includes_order_and_username(order, custom_user):
    """
    __str__ should read:
      "Review for Order #<id> by <username>"
    """
    review = Review.objects.create(order=order)
    expected = f"Review for Order #{order.id} by {custom_user.username}"
    assert str(review) == expected


@pytest.mark.django_db
def test_reverse_relation(order):
    """
    order.review should return the Review instance.
    """
    review = Review.objects.create(order=order)
    assert order.review == review


@pytest.mark.django_db
def test_unique_order_constraint(order):
    """
    You cannot create two Reviews for the same Order.
    """
    Review.objects.create(order=order)
    with pytest.raises(IntegrityError):
        Review.objects.create(order=order)


@pytest.mark.django_db
def test_negative_rating_validation(order):
    """
    rating < 0 should not pass model validation.
    """
    review = Review(order=order, rating=-1)
    with pytest.raises(ValidationError):
        review.full_clean()


@pytest.mark.django_db
def test_non_integer_rating_validation(order):
    """
    A non-integer rating should fail validation.
    """
    review = Review(order=order, rating="bad")
    with pytest.raises(ValidationError):
        review.full_clean()


@pytest.mark.django_db
def test_cascade_delete_order_deletes_review(order):
    """
    Deleting the Order should automatically delete its Review.
    """
    review = Review.objects.create(order=order)
    order.delete()
    assert not Review.objects.filter(pk=review.pk).exists()


@pytest.mark.django_db
def test_unicode_comment_preserved(order):
    """
    Non-ASCII characters in comment should be stored unchanged.
    """
    text = "Fantastic! 🌟👍"
    review = Review.objects.create(order=order, comment=text)
    assert review.comment == text
