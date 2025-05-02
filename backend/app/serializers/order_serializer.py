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

    unwanted_ingredient_names = serializers.SerializerMethodField()
    category = serializers.CharField(source="item.category", read_only=True)

    class Meta:
        model = OrderItem
        fields = ["item_id", "item_name", "quantity", "unwanted_ingredients", "unwanted_ingredient_names", "category"]

    def get_unwanted_ingredient_names(self, obj):
        return [ingredient.name for ingredient in obj.unwanted_ingredients.all()]


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

    food_eta_minutes = serializers.IntegerField(read_only=True)
    beverage_eta_minutes = serializers.IntegerField(read_only=True)

    estimated_food_ready_time = serializers.DateTimeField(read_only=True)
    estimated_beverage_ready_time = serializers.DateTimeField(read_only=True)
    
    worker_name = serializers.CharField(source="worker.name", read_only=True)
    reviewed = serializers.BooleanField(read_only=True)

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
            "food_status",
            "beverage_status",
            "total_price",
            "order_items",
            "estimated_food_ready_time",
            "estimated_beverage_ready_time",
            "food_eta_minutes",
            "beverage_eta_minutes",
            "reviewed",
            "worker_name",
        ]

    def get_worker_name(self, obj):
        return obj.worker.name if obj.worker else None

    def create(self, validated_data):
        order_items_data = validated_data.pop("order_items")
        order = Order.objects.create(**validated_data)

        for item_data in order_items_data:
            unwanted_ingredients = item_data.pop("unwanted_ingredients", [])
            order_item = OrderItem.objects.create(order=order, **item_data)
            order_item.unwanted_ingredients.set(unwanted_ingredients)
        return order
