# app/models/promotion_models.py

from django.db import models
from .restaurant_models import Restaurant  # Adjust import based on structure

class PromotionNotification(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="promotions"
    )
    title = models.CharField(max_length=255)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    sent = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.restaurant.name}"