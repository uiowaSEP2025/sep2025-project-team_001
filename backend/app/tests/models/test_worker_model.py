import pytest
from app.models.worker_models import Worker
from django.core.exceptions import ValidationError


@pytest.mark.django_db
def test_worker_str(worker):
    """
    __str__ returns "<Role Title> for <username> (PIN: <pin>)"
    using the `worker` fixture.
    """
    expected = f"{worker.role.title()} for {worker.restaurant.user.username} (PIN: {worker.pin})"
    assert str(worker) == expected


@pytest.mark.django_db
def test_worker_belongs_to_restaurant(worker, restaurant):
    """
    The Worker appears in the restaurant.workers reverse relation.
    """
    assert worker in restaurant.workers.all()


@pytest.mark.django_db
def test_cascade_delete_restaurant_deletes_worker(worker, restaurant):
    """
    Deleting the Restaurant cascades to remove its Workers.
    """
    pk = worker.pk
    restaurant.delete()
    assert not Worker.objects.filter(pk=pk).exists()


@pytest.mark.django_db
def test_role_choices_validation(restaurant):
    """
    Assigning a role outside ROLE_CHOICES should raise ValidationError.
    """
    w = Worker(restaurant=restaurant, name="Alice", pin="1234", role="chef")
    with pytest.raises(ValidationError):
        w.full_clean()


@pytest.mark.django_db
def test_pin_length_and_content_validation(restaurant):
    """
    PIN must not exceed 4 characters and cannot be blank.
    Shorter pins (e.g. 3 digits) are allowed.
    """
    # Too long → fails
    w1 = Worker(restaurant=restaurant, name="Bob", pin="12345", role="manager")
    with pytest.raises(ValidationError):
        w1.full_clean()

    # Too short (3 chars) → should pass
    w2 = Worker(restaurant=restaurant, name="Bob", pin="123", role="manager")
    w2.full_clean()  # no exception

    # Blank → fails
    w3 = Worker(restaurant=restaurant, name="Bob", pin="", role="manager")
    with pytest.raises(ValidationError):
        w3.full_clean()


@pytest.mark.django_db
def test_name_required_and_max_length(restaurant):
    """
    Name is required (blank fails) and max_length=100 enforced.
    """
    # Blank name
    w1 = Worker(restaurant=restaurant, name="", pin="0000", role="bartender")
    with pytest.raises(ValidationError):
        w1.full_clean()

    # Overlong name
    long_name = "x" * 101
    w2 = Worker(restaurant=restaurant, name=long_name, pin="0000", role="bartender")
    with pytest.raises(ValidationError):
        w2.full_clean()


@pytest.mark.django_db
def test_unicode_name_and_str(restaurant, custom_user):
    """
    Unicode in name should be preserved, and __str__ still works.
    """
    restaurant.user = custom_user
    restaurant.save()
    w = Worker.objects.create(
        restaurant=restaurant,
        name="José 🚀",
        pin="9999",
        role="bartender"
    )
    # Name stored correctly
    assert w.name == "José 🚀"
    # __str__ unaffected by unicode name
    expected = f"{w.role.title()} for {restaurant.user.username} (PIN: {w.pin})"
    assert str(w) == expected
