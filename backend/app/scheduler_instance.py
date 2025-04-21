# app/scheduler_instance.py

# Dictionary to hold scheduler instances keyed by restaurant id
restaurant_schedulers = {}


def get_restaurant_scheduler(restaurant_id, num_bartenders=2):
    """
    Retrieve the scheduler instance for the given restaurant.
    If one doesn't exist, create it with the default number of bartenders.
    """
    if restaurant_id not in restaurant_schedulers:
        from app.utils.multi_bartender_scheduler import MultiBartenderScheduler
        restaurant_schedulers[restaurant_id] = MultiBartenderScheduler(num_bartenders=num_bartenders)
    return restaurant_schedulers[restaurant_id]
