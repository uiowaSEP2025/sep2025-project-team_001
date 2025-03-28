from rest_framework import serializers

from app.models.customer_models import Customer
from app.models.order_models import Order, OrderItem
from app.models.restaurant_models import Restaurant, Item


class OrderItemSerializer(serializers.ModelSerializer):
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(), source='item', write_only=True
    )
    item = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['item_id', 'item', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source='customer', write_only=True
    )
    restaurant_id = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(), source='restaurant', write_only=True
    )
    order_items = OrderItemSerializer(many=True, write_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_id', 'restaurant_id', 'start_time', 'status', 'order_items']

    def create(self, validated_data):
        order_items_data = validated_data.pop('order_items')
        order = Order.objects.create(**validated_data)

        for item_data in order_items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order
