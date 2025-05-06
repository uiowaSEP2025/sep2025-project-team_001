# urls.py
from app.mobileViews.notificationViews import save_fcm_token
from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .mobileViews.mobileViews import login_customer, register_customer
from .mobileViews.stripeViews import create_payment_intent, delete_payment_method, list_saved_payment_methods, pay_with_saved_card
from .views.auth_views import login_restaurant, login_user, register_user, validate_business
from .views.menu_views import manage_menu_item, menu_items_api, get_item_statistics
from .views.orders_views import (
    create_order,
    estimate_order_eta,
    get_customer_orders,
    get_order,
    retrieve_active_orders,
    update_order_category_status,
    update_order_status,
)
from .views.restaurant_views import get_menu_items, get_restaurant, get_restaurants
from .views.review_views import create_review, list_reviews
from .views.stats_views import daily_stats, get_bartender_statistics, get_item_statistics, get_restaurant_statistics
from .views.worker_views import create_worker, delete_worker, get_workers, update_worker
from .views.promotion_views import list_promotions, create_promotion, update_promotion, delete_promotion, send_promotion


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
    path("restaurant/<int:restaurant_id>/", get_restaurant, name="get_restaurant"),
    
    path("mobile/fcm_token/", save_fcm_token, name="save_fcm_token"),
    
    path("order/new/", create_order, name="create_order"),
    path("order/customer/", get_customer_orders, name="get_customer_orders"),
    path("order/payment/", create_payment_intent, name="create_payment"),
    path("order/payment/methods/", list_saved_payment_methods, name="list_saved_payment_methods"),
    path("order/payment/saved_card/", pay_with_saved_card, name="pay_with_saved_card"),
    path("order/payment/saved_card/<str:payment_method_id>/", delete_payment_method, name="pay_with_saved_card"),
    path("order/<int:order_id>/", get_order, name="get_order"),
    path("order/estimate/", estimate_order_eta, name="estimate_order_eta"),
    
    # api
    path("api/menu-items/", menu_items_api, name="menu_items_api"),
    path("api/manage-item/", manage_menu_item, name="manage_menu_item"),
    path("retrieve/orders/", retrieve_active_orders, name="retrieve_active_orders"),
    path("orders/<int:restaurant_id>/<int:order_id>/<str:new_status>/", update_order_status, name="update_order_status"),
    path("orders/<int:restaurant_id>/<int:order_id>/<str:category>/<str:new_status>/", update_order_category_status, name="update_order_category_status"),
    path("create-worker/", create_worker, name="create_worker"),
    path("reviews/", list_reviews, name="list_reviews"),
    path("get-workers/", get_workers, name="get_workers"),
    path('update-worker/<int:worker_id>/', update_worker),
    path("delete-worker/<int:worker_id>/", delete_worker, name="delete_worker"),
    path("daily_stats", daily_stats, name="daily_stats"),
    path('api/statistics/', get_item_statistics, name="get_item_statistics"),
    path('bartender-statistics/', get_bartender_statistics, name="get_bartender_statistics"),
    path('restaurant-statistics/', get_restaurant_statistics, name="get_restaurant_statistics"),
    path("promotions/", list_promotions, name="list_promotions"),
    path("promotions/create/", create_promotion, name="create_promotion"),
    path("promotions/<int:promotion_id>/update/", update_promotion, name="update_promotion"),
    path("promotions/<int:promotion_id>/delete/", delete_promotion, name="delete_promotion"),
    path("promotions/<int:promotion_id>/send/", send_promotion, name="send_promotion"),
]
