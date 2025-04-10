import pytest
from app.models.worker_models import Worker


@pytest.mark.django_db
def test_worker_str(restaurant):
    """
    Ensure Worker.__str__ returns the expected formatted string.
    """
    worker = Worker.objects.create(
        restaurant=restaurant,
        role="manager",
        pin="1234"
    )
    expected_str = f"Manager for {restaurant.user.username} (PIN: 1234)"
    assert str(worker) == expected_str


@pytest.mark.django_db
def test_worker_role_choices(restaurant):
    """
    Ensure Worker role choices are respected and stored correctly.
    """
    manager = Worker.objects.create(restaurant=restaurant, role="manager", pin="1111")
    bartender = Worker.objects.create(restaurant=restaurant, role="bartender", pin="2222")

    assert manager.role == "manager"
    assert bartender.role == "bartender"


@pytest.mark.django_db
def test_worker_restaurant_link(restaurant):
    """
    Ensure a Worker is linked to the correct restaurant and accessible via reverse relationship.
    """
    worker = Worker.objects.create(restaurant=restaurant, role="manager", pin="3333")
    assert worker.restaurant == restaurant
    assert worker in restaurant.workers.all()
