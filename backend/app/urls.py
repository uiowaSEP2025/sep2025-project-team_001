# urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .mobileViews.mobileViews import register_customer, login_customer
from app.views.auth_views import login_user, register_user
from app.views.restaurant_views import get_menu_items, get_restaurants
from app.views.orders_views import create_order
from app.views.menu_views import menu_items_api, manage_menu_item

urlpatterns = [
    path('login/', login_user, name='login'),
    path('register/', register_user, name='register'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
   
#    mobile
    path('mobile/register/', register_customer, name='customerRegister'),
    path('mobile/login/', login_customer, name='customerLogin'),    
    path('restaurants/list', get_restaurants, name= 'get_restaurants'),
    path('restaurants/<str:restaurant>/menu/', get_menu_items, name= "get_menu_items"), 
    path('order/new/', create_order , name='create_order'),       
    
# api
    path('api/menu-items/', menu_items_api, name='menu_items_api'),
    path('api/manage-item/', manage_menu_item, name='manage_menu_item'),
]
