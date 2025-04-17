from rest_framework import serializers
from ..models.review_models import Review

class ReviewSerializer(serializers.ModelSerializer):
    customer_name = serializers.CharField(source='order.customer.user.first_name', read_only=True)
    worker_name = serializers.CharField(source='order.worker.name', read_only=True)
    items = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = ['id', 'order', 'rating', 'comment', 'created_at', 'customer_name', 'worker_name', 'items']

    def get_items(self, obj):
        return [oi.item.name for oi in obj.order.order_items.all()]
