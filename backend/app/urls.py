from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import login_user, register_user
from .mobileViews.mobileViews import register_customer, login_customer


urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path('mobile/register/', register_customer, name='customerRegister'),
    path('mobile/login/', login_customer, name='customerLogin')
]
