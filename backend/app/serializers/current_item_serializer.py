from rest_framework import serializers
from app.models import CurrentItem

class CurrentItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CurrentItem
        fields = ['id', 'item_name', 'quantity', 'status', 'created_at']