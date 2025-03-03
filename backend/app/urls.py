from django.urls import path
from .views import login_user, register_user
from .customer_views import get_customers, get_customer_detail

urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('customers/', get_customers, name='customer-list'),
    path('customers/<int:pk>/', get_customer_detail, name='customer-detail'),
]

