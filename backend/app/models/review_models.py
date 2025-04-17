from django.db import models

from .order_models import Order


class Review(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='review')
    rating = models.PositiveIntegerField(default=5)  # 1-5 scale
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Review for Order #{self.order.id} by {self.order.customer.user.username}"
