# urls.py
from app.mobileViews.notificationViews import save_fcm_token
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .mobileViews.mobileViews import login_customer, register_customer
from .mobileViews.stripeViews import create_payment_intent, create_setup_intent
from .views.auth_views import login_restaurant, login_user, register_user, validate_business
from .views.menu_views import manage_menu_item, menu_items_api, get_item_statistics
from .views.orders_views import create_order, estimate_order_eta, get_customer_orders, retrieve_active_orders, update_order_status
from .views.restaurant_views import get_menu_items, get_restaurants
from .views.review_views import create_review, list_reviews
from .views.stats_views import daily_stats
from .views.worker_views import create_worker, delete_worker, get_workers, update_worker


urlpatterns = [
   path("login_restaurant/", login_restaurant, name="login_restaurant"),
    path("login_user/", login_user, name="login_user"),
    path("register/", register_user, name="register"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("validate_restaurant/", validate_business, name="validate_restaurant"),
    # mobile
    path("mobile/register/", register_customer, name="customerRegister"),
    path("mobile/login/", login_customer, name="customerLogin"),
    path("mobile/review/create", create_review, name="create_review"),
    path("restaurants/list/", get_restaurants, name="get_restaurants"),
    path("restaurants/<int:restaurant_id>/menu/", get_menu_items, name="get_menu_items"),
    path("order/new/", create_order, name="create_order"),
    path("order/customer/", get_customer_orders, name="get_customer_orders"),
    path("order/payment/", create_payment_intent, name="create_payment"),
    path("order/setup/", create_setup_intent, name="create_setup_intent"),
    path("mobile/fcm_token/", save_fcm_token, name="save_fcm_token"),

    path("order/estimate/", estimate_order_eta, name="estimate_order_eta"),
    # api
    path("api/menu-items/", menu_items_api, name="menu_items_api"),
    path("api/manage-item/", manage_menu_item, name="manage_menu_item"),
    path("retrieve/orders/", retrieve_active_orders, name="retrieve_active_orders"),
    path("orders/<int:restaurant_id>/<int:order_id>/<str:new_status>/", update_order_status,
         name="update_order_status"),
    path("create-worker/", create_worker, name="create_worker"),
    path("reviews/", list_reviews, name="list_reviews"),
    path("get-workers/", get_workers, name="get_workers"),
    path('update-worker/<int:worker_id>/', update_worker),
    path("delete-worker/<int:worker_id>/", delete_worker, name="delete_worker"),
    path("daily_stats", daily_stats, name="daily_stats"),
    path('api/statistics/', get_item_statistics, name="get_item_statistics"),
]
