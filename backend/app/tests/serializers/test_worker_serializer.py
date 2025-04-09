import pytest
from app.models.worker_models import Worker
from app.serializers.worker_serializer import WorkerSerializer


@pytest.mark.django_db
def test_worker_serializer_output(restaurant):
    """
    WorkerSerializer should correctly serialize a Worker instance.
    """
    worker = Worker.objects.create(
        restaurant=restaurant,
        pin="1234",
        role="manager"
    )
    serializer = WorkerSerializer(worker)
    data = serializer.data

    assert data["id"] == worker.id
    assert data["restaurant"] == restaurant.id
    assert data["pin"] == "1234"
    assert data["role"] == "manager"


@pytest.mark.django_db
def test_worker_serializer_input_valid(restaurant):
    """
    Valid input should create a Worker instance through deserialization.
    """
    payload = {
        "restaurant": restaurant.id,
        "pin": "5678",
        "role": "bartender"
    }
    serializer = WorkerSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors
    worker = serializer.save()

    assert worker.restaurant == restaurant
    assert worker.pin == "5678"
    assert worker.role == "bartender"


@pytest.mark.django_db
def test_worker_serializer_invalid_role(restaurant):
    """
    Invalid role value should cause validation to fail.
    """
    payload = {
        "restaurant": restaurant.id,
        "pin": "0000",
        "role": "chef"  # invalid
    }
    serializer = WorkerSerializer(data=payload)
    assert not serializer.is_valid()
    assert "role" in serializer.errors
