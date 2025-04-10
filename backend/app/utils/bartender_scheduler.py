# app/utils/bartender_scheduler.py

from datetime import timedelta


class BartenderScheduler:
    def __init__(self):
        # Busy intervals stored as tuples of (start_dt, end_dt)
        self.busy_intervals = []

    def add_order(self, start_dt, duration_minutes):
        """
        :param start_dt: datetime when order starts
        :param duration_minutes: integer minutes for order duration
        """
        end_dt = start_dt + timedelta(minutes=duration_minutes)
        self.busy_intervals.append((start_dt, end_dt))
        self.busy_intervals.sort(key=lambda interval: interval[0])

    def find_free_slot(self, now_dt, required_duration_minutes):
        """
        Returns the earliest datetime >= now_dt where a slot of required_duration_minutes is free.
        """
        slot_start = now_dt
        for busy_start, busy_end in self.busy_intervals:
            gap = (busy_start - slot_start).total_seconds() / 60
            if gap > required_duration_minutes:
                return slot_start
            if slot_start < busy_end:
                slot_start = busy_end
        return slot_start
