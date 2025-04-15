from django.db import models
from .order_models import Order
from .restaurant_models import Item, Worker

class Review(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='review')
    worker = models.ForeignKey(Worker, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviews')
    items = models.ManyToManyField(Item, related_name='reviewed_in', blank=True)  # Items mentioned in the review

    rating = models.PositiveIntegerField(default=5)  # 1-5 scale
    comment = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for Order #{self.order.id} by {self.order.customer.user.username}"
