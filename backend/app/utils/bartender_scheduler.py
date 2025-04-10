# app/utils/bartender_scheduler.py

class BartenderScheduler:
    def __init__(self):
        # Busy intervals stored as tuples: (start_minute, end_minute)
        self.busy_intervals = []

    def add_order(self, start_time, duration):
        """
        Add a busy interval for an order.
        :param start_time: The time (in minutes) when the order starts.
        :param duration: The duration (in minutes) of the order.
        """
        end_time = start_time + duration
        self.busy_intervals.append((start_time, end_time))
        # Keep intervals sorted by start time.
        self.busy_intervals.sort(key=lambda interval: interval[0])

    def find_free_slot(self, current_time, required_duration):
        """
        Returns the earliest start time from current_time where a slot of required_duration is free.
        :param current_time: Current time in minutes.
        :param required_duration: Duration needed (in minutes).
        :return: The start time in minutes when the bartender can start the new order.
        """
        available_start = current_time

        # Iterate over busy intervals to find a gap that's large enough.
        for busy_start, busy_end in self.busy_intervals:
            # If there is enough gap between available_start and the next busy interval...
            if busy_start - available_start > required_duration:
                return available_start
            else:
                # Move available_start to after the current busy interval if it overlaps
                if available_start < busy_end:
                    available_start = busy_end

        # No gap found; the new order can start after the last busy period.
        return available_start
