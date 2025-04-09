from rest_framework import serializers

from ..models.worker_models import Worker


class WorkerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Worker
        fields = ['id', 'restaurant', 'pin', 'role']
