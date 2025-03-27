# backend/app/models.py

from django.contrib.auth.models import AbstractUser
from django.db import models

# Has username, email, password, first_name, last_name
class CustomUser(AbstractUser):
    pass

class Manager(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="manager")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    #create string rep of this object
    def __str__(self):
        return f"{self.user.username} (Manager)"


class Customer(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name="customer")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.user.username,
            "email": self.user.email,
            "phone": self.user.phone,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    def __str__(self):
        return f"{self.user.username}'s Customer Profile"