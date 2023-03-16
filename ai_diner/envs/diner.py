import numpy as np
class Diner:
    def __init__(self, dining_time: int, dining_hall_count: int, day_tracker: dict):
        self.dining_time = dining_time
        self.prev_dining_hall = None

    def visit_dining_hall(self, dining_hall_id:int):
        self.prev_dining_hall = dining_hall_id
    
    def get_eating_time(self):
        return self.dining_time
    