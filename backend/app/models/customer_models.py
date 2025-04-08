# backend/app/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models


# Has username, email, password, first_name, last_name
class CustomUser(AbstractUser):
    pass


class Customer(models.Model):
    user = models.OneToOneField(
        CustomUser, on_delete=models.CASCADE, related_name="customer"
    )
    stripe_customer_id = models.CharField(
        max_length=255, null=True, blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.user.first_name,
            "username": self.user.username,
            "email": self.user.email,
            "phone": self.user.phone,
            "stripe_customer_id": self.stripe_customer_id,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def __str__(self):
        return f"{self.user.username}'s Customer Profile"
