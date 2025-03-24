from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from app.views.auth_views import login_user, register_user
from app.views.orders_views import CurrentItemsList

urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('bartender_view/', CurrentItemsList.as_view(), n