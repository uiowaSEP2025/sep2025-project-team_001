from django.db import models
from .customer_models import Customer
from app.models.customer_models import Manager

class Restaurant(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    managers = models.ManyToManyField(Manager, related_name="restaurants")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

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


    
class OrderItems(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.CASCADE,
        related_name="orders"
    )

    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name="orders"
    )
    quantity = models.IntegerField()

    cost = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return f"{self.quantity} of {self.item.name} from {self.restaurant.name}"
    
class CurrentItem(models.Model):
    item_name = models.CharField(max_length=100)
    quantity = models.PositiveIntegerField(default=1)
    status = models.CharField(max_length=20, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.item_name} ({self.quantity})"
