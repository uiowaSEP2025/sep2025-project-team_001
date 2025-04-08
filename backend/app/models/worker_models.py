from django.db import models
from ..models.restaurant_models import Restaurant

class Worker(models.Model):
    ROLE_CHOICES = [
        ('manager', 'Manager'),
        ('bartender', 'Bartender'),
    ]

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='workers')
    pin = models.CharField(max_length=4)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.role.title()} for {self.restaurant.user.username} (PIN: {self.pin})"
