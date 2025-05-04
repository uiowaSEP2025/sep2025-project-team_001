from rest_framework import serializers
from app.models import PromotionNotification

class PromotionNotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PromotionNotification
        fields = '__all__'