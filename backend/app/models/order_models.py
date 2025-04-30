from django.db import models

from .customer_models import Customer
from .restaurant_models import Ingredient, Item, Restaurant
from .worker_models import Worker


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.CASCADE, related_name="orders"
    )
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="orders"
    )
    start_time = models.DateTimeField(auto_now_add=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True, related_name="orders")

    food_eta_minutes = models.PositiveIntegerField(null=True, blank=True)
    beverage_eta_minutes = models.PositiveIntegerField(null=True, blank=True)

    estimated_food_ready_time = models.DateTimeField(null=True, blank=True)
    estimated_beverage_ready_time = models.DateTimeField(null=True, blank=True)

    status = models.CharField(max_length=50, default="pending")
    food_status = models.CharField(
        max_length=50,
        choices=[
            ("pending", "Pending"),
            ("completed", "Completed"),
            ("picked_up", "Picked Up"),
        ],
        default="pending",
    )

    beverage_status = models.CharField(
        max_length=50,
        choices=[
            ("pending", "Pending"),
            ("completed", "Completed"),
            ("picked_up", "Picked Up"),
        ],
        default="pending",
    )


    def __str__(self):
        return f"Order #{self.id} by {self.customer.user.username} at {self.restaurant.name}"

    def get_total(self):
        return sum(item.item.price * item.quantity for item in self.order_items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name="order_items"
    )
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    unwanted_ingredients = models.ManyToManyField(
        Ingredient, blank=True, related_name="excluded_from_order_items"
    )

    def __str__(self):
        return f"{self.quantity}x {self.item.name} (Order #{self.order.id})"
