# urls.py
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .mobileViews.mobileViews import login_customer, register_customer
from .views.auth_views import login_user, register_user
from .views.menu_views import manage_menu_item, menu_items_api
from .views.orders_views import (
    create_order,
    get_customer_orders,
    mark_order_completed,
    retrieve_active_orders,
)
from .views.restaurant_views import get_menu_items, get_restaurants

urlpatterns = [
    path("login/", login_user, name="login"),
    path("register/", register_user, name="register"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    # mobile
    path("mobile/register/", register_customer, name="customerRegister"),
    path("mobile/login/", login_customer, name="customerLogin"),
    path("restaurants/list/", get_restaurants, name="get_restaurants"),
    path("restaurants/<str:restaurant>/menu/", get_menu_items, name="get_menu_items"),
    path("order/new/", create_order, name="create_order"),
    path("order/customer/", get_customer_orders, name="get_customer_orders"),
    # api
    path("api/menu-items/", menu_items_api, name="menu_items_api"),
    path("api/manage-item/", manage_menu_item, name="manage_menu_item"),
    path("retrieve/orders/", retrieve_active_orders, name="retrieve_active_orders"),
    path(
        "orders/<int:order_id>/complete/",
        mark_order_completed,
        name="mark_order_completed",
    ),  # <int:... passed to view as the order_id
]
