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
        name="Test Worker",
        pin="1234",
        role="manager"
    )
    serializer = WorkerSerializer(worker)
    data = serializer.data

    assert data["id"] == worker.id
    assert data["restaurant"] == restaurant.id
    assert data["name"] == "Test Worker"
    assert data["pin"] == "1234"
    assert data["role"] == "manager"


@pytest.mark.django_db
def test_worker_serializer_input_valid(restaurant):
    """
    Valid input should deserialize and create a Worker instance.
    """
    payload = {
        "restaurant": restaurant.id,
        "name": "John Doe",
        "pin": "5678",
        "role": "bartender"
    }
    serializer = WorkerSerializer(data=payload)
    assert serializer.is_valid(), serializer.errors
    worker = serializer.save()

    assert worker.restaurant == restaurant
    assert worker.name == "John Doe"
    assert worker.pin == "5678"
    assert worker.role == "bartender"


@pytest.mark.django_db
def test_worker_serializer_invalid_role(restaurant):
    """
    Invalid role value should cause validation to fail.
    """
    payload = {
        "restaurant": restaurant.id,
        "name": "John Doe",
        "pin": "0000",
        "role": "chef"  # invalid
    }
    serializer = WorkerSerializer(data=payload)
    assert not serializer.is_valid()
    assert "role" in serializer.errors


@pytest.mark.django_db
def test_worker_serializer_missing_name(restaurant):
    """
    Omitting 'name' should cause validation to fail.
    """
    payload = {
        "restaurant": restaurant.id,
        "pin": "0000",
        "role": "bartender"
    }
    serializer = WorkerSerializer(data=payload)
    assert not serializer.is_valid()
    assert "name" in serializer.errors


@pytest.mark.django_db
def test_worker_serializer_missing_pin(restaurant):
    """
    Omitting 'pin' should cause validation to fail.
    """
    payload = {
        "restaurant": restaurant.id,
        "name": "John Doe",
        "role": "bartender"
    }
    serializer = WorkerSerializer(data=payload)
    assert not serializer.is_valid()
    assert "pin" in serializer.errors


@pytest.mark.django_db
def test_worker_serializer_missing_role(restaurant):
    """
    Omitting 'role' should cause validation to fail.
    """
    payload = {
        "restaurant": restaurant.id,
        "name": "John Doe",
        "pin": "0000",
    }
    serializer = WorkerSerializer(data=payload)
    assert not serializer.is_valid()
    assert "role" in serializer.errors


@pytest.mark.django_db
def test_name_max_length_serializer(restaurant):
    """
    Name longer than 100 chars should fail validation.
    """
    long_name = "x" * 101
    payload = {
        "restaurant": restaurant.id,
        "name": long_name,
        "pin": "1234",
        "role": "manager"
    }
    serializer = WorkerSerializer(data=payload)
    assert not serializer.is_valid()
    assert "name" in serializer.errors


@pytest.mark.django_db
def test_pin_max_length_serializer(restaurant):
    """
    Pin longer than 4 chars should fail validation.
    """
    payload = {
        "restaurant": restaurant.id,
        "name": "Jane Doe",
        "pin": "12345",
        "role": "manager"
    }
    serializer = WorkerSerializer(data=payload)
    assert not serializer.is_valid()
    assert "pin" in serializer.errors
