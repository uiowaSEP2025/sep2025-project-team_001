from datetime import timedelta

from app.models.order_models import Order, OrderItem
from app.models.restaurant_models import Item
from app.utils.order_eta_utils import recalculate_pending_etas
from django.utils import timezone


def make_order(restaurant, customer, food_qty=0, bev_qty=0):
    """
    Helper: create one Order + its OrderItems for given food/bev quantities.
    """
    order = Order.objects.create(
        restaurant=restaurant,
        customer=customer,
        status="pending"
    )
    if food_qty:
        food = Item.objects.create(
            name="Food", category="food", price=1.0, restaurant=restaurant
        )
        OrderItem.objects.create(order=order, item=food, quantity=food_qty)
    if bev_qty:
        bev = Item.objects.create(
            name="Drink", category="beverage", price=1.0, restaurant=restaurant
        )
        OrderItem.objects.create(order=order, item=bev, quantity=bev_qty)
    return order


def test_no_pending_orders_runs_silently(restaurant, customer):
    # No pending orders—should not raise
    recalculate_pending_etas(restaurant.id, num_bartenders=2)


def test_single_order_food_and_bev(restaurant, customer):
    now = timezone.now().replace(second=0, microsecond=0)
    order = make_order(restaurant, customer, food_qty=2, bev_qty=3)

    recalculate_pending_etas(restaurant.id, num_bartenders=1)
    order.refresh_from_db()

    # ETAs should both be >= now, and not equal to each other
    assert order.estimated_food_ready_time >= now
    assert order.estimated_beverage_ready_time >= now
    assert order.estimated_food_ready_time != order.estimated_beverage_ready_time


def test_multiple_orders_beverage_sequential(restaurant, customer):
    now = timezone.now().replace(second=0, microsecond=0)
    o1 = make_order(restaurant, customer, bev_qty=2)
    o2 = make_order(restaurant, customer, bev_qty=2)

    recalculate_pending_etas(restaurant.id, num_bartenders=1)
    o1.refresh_from_db()
    o2.refresh_from_db()

    # First ready at now+2m, second at now+4m
    expected1 = now + timedelta(minutes=2)
    expected2 = now + timedelta(minutes=4)
    assert o1.estimated_beverage_ready_time == expected1
    assert o2.estimated_beverage_ready_time == expected2


def test_multiple_orders_with_two_bartenders(restaurant, customer):
    now = timezone.now().replace(second=0, microsecond=0)
    o1 = make_order(restaurant, customer, bev_qty=3)
    o2 = make_order(restaurant, customer, bev_qty=3)
    o3 = make_order(restaurant, customer, bev_qty=3)

    recalculate_pending_etas(restaurant.id, num_bartenders=2)
    o1.refresh_from_db()
    o2.refresh_from_db()
    o3.refresh_from_db()

    # First two finish at now+3m, third at now+6m
    expected3 = now + timedelta(minutes=3)
    expected6 = now + timedelta(minutes=6)
    assert o1.estimated_beverage_ready_time == expected3
    assert o2.estimated_beverage_ready_time == expected3
    assert o3.estimated_beverage_ready_time == expected6


def test_food_only_order(restaurant, customer):
    now = timezone.now().replace(second=0, microsecond=0)
    order = make_order(restaurant, customer, food_qty=3, bev_qty=0)
    recalculate_pending_etas(restaurant.id, num_bartenders=1)
    order.refresh_from_db()
    # food=15+2*3=21→round 25
    assert order.estimated_food_ready_time == now + timedelta(minutes=25)
    assert order.food_eta_minutes == 25
    # no beverages
    assert order.estimated_beverage_ready_time is None
    assert order.beverage_eta_minutes is None


def test_beverage_only_order(restaurant, customer):
    now = timezone.now().replace(second=0, microsecond=0)
    order = make_order(restaurant, customer, food_qty=0, bev_qty=4)
    recalculate_pending_etas(restaurant.id, num_bartenders=1)
    order.refresh_from_db()
    # beverage raw=4 → finish at now+4 → delta=4 → round‐delta stored as raw minutes
    assert order.estimated_beverage_ready_time == now + timedelta(minutes=4)
    assert order.beverage_eta_minutes == 4
    # no food
    assert order.estimated_food_ready_time is None
    assert order.food_eta_minutes is None
