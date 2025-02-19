# app/urls.py

from django.urls import path
from .views import login  # Import the login view

urlpatterns = [
    path('login/', login, name='login'),  # Map the /login endpoint to the login view
]
