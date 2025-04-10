# app/utils/multi_bartender_scheduler.py

from app.utils.bartender_scheduler import BartenderScheduler


class MultiBartenderScheduler:
    def __init__(self, num_bartenders=1):
        # Initialize a scheduler instance for each bartender.
        self.schedulers = [BartenderScheduler() for _ in range(num_bartenders)]

    def find_best_free_slot(self, current_time, required_duration):
        """
        Find the best (earliest) free slot among all bartenders.
        :param current_time: The current time in minutes.
        :param required_duration: The duration required in minutes.
        :return: A tuple (free_start_time, bartender_index) for the earliest available slot.
        """
        best_start = None
        best_index = None

        for index, scheduler in enumerate(self.schedulers):
            candidate_start = scheduler.find_free_slot(current_time, required_duration)
            if best_start is None or candidate_start < best_start:
                best_start = candidate_start
                best_index = index

        return best_start, best_index

    def add_order_to_bartender(self, bartender_index, start_time, duration):
        """
        Assign an order to the specified bartender.
        :param bartender_index: Which bartender (index) should take the order.
        :param start_time: The order's start time in minutes.
        :param duration: The order's duration in minutes.
        """
        self.schedulers[bartender_index].add_order(start_time, duration)
