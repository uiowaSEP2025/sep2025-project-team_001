from rest_framework import serializers

from ..models.customer_models import Customer
from ..models.order_models import Order, OrderItem
from ..models.restaurant_models import Ingredient, Item, Restaurant


class OrderItemSerializer(serializers.ModelSerializer):
    item_id = serializers.PrimaryKeyRelatedField(
        queryset=Item.objects.all(), source="item", write_only=True
    )
    item_name = serializers.CharField(source="item.name", read_only=True)
    unwanted_ingredients = serializers.PrimaryKeyRelatedField(
        queryset=Ingredient.objects.all(), many=True, required=False
    )

    class Meta:
        model = OrderItem
        fields = ["item_id", "item_name", "quantity", "unwanted_ingredients"]


class OrderSerializer(serializers.ModelSerializer):
    # Fields for creating orders
    customer_id = serializers.PrimaryKeyRelatedField(
        queryset=Customer.objects.all(), source="customer", write_only=True
    )
    restaurant_id = serializers.PrimaryKeyRelatedField(
        queryset=Restaurant.objects.all(), source="restaurant", write_only=True
    )
    
    
    
    # Fields for displaying orders
    customer_name = serializers.CharField(
        source="customer.user.first_name", read_only=True
    )
    restaurant_name = serializers.CharField(source="restaurant.name", read_only=True)
    
    restaurant_id_read = serializers.IntegerField(source="restaurant.id", read_only=True)

    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "customer_id",
            "restaurant_id",
            "restaurant_id_read",
            "customer_name",
            "restaurant_name",
            "start_time",
            "status",
            "total_price",
            "order_items",
        ]

    def create(self, validated_data):
        order_items_data = validated_data.pop("order_items")
        order = Order.objects.create(**validated_data)

        for item_data in order_items_data:
            unwanted_ingredients = item_data.pop("unwanted_ingredients", [])
            order_item = OrderItem.objects.create(order=order, **item_data)
            order_item.unwanted_ingredients.set(unwanted_ingredients)
        return order
