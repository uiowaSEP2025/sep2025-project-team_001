from django.db import models

from .customer_models import Customer, Manager


class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    managers = models.ManyToManyField(Manager, related_name="restaurants")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    restaurant_image = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Item(models.Model):
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="items"
    )
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, blank=True)  # e.g., drink or food'
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    base64_image = models.TextField(blank=True, null=True)

    def __str__(self):
        image_preview = self.base64_image[:30] + "..." if self.base64_image else "No image"
        return f"{self.name} (Image: {image_preview})"
