# app/utils/multi_bartender_scheduler.py

class MultiBartenderScheduler:
    def __init__(self, num_bartenders=1):
        from app.utils.bartender_scheduler import BartenderScheduler
        self.schedulers = [BartenderScheduler() for _ in range(num_bartenders)]

    def find_best_free_slot(self, now_dt, duration_minutes):
        best_start = None
        best_idx = None
        for idx, sched in enumerate(self.schedulers):
            candidate = sched.find_free_slot(now_dt, duration_minutes)
            if best_start is None or candidate < best_start:
                best_start, best_idx = candidate, idx
        return best_start, best_idx

    def add_order_to_bartender(self, idx, start_dt, duration_minutes):
        self.schedulers[idx].add_order(start_dt, duration_minutes)
