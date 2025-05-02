from django.db import models

from .customer_models import CustomUser


class Restaurant(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="restaurant",
    )
    name = models.CharField(max_length=255)  # Business name
    address = models.CharField(max_length=255)
    phone = models.CharField(max_length=50)
    restaurant_image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="items"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, blank=True)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    item_image_url = models.URLField(blank=True, null=True)
    times_ordered = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.name} (Image: {self.item_image_url or 'No image'})"


class Ingredient(models.Model):
    item = models.ForeignKey(Item, on_delete=models.CASCADE, related_name='ingredients')
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
