from app.models import PromotionNotification
from rest_framework import serializers


class PromotionNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionNotification
        fields = '__all__'
