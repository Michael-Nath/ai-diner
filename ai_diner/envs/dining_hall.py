import numpy as np
class DiningHall:
    def __init__(self, day_tracker: dict):
        self.headcount = 0
        self.day_tracker = day_tracker
        self.special_probs = np.random.rand(self.day_tracker['total_days'])
        self.determine_special()

    def determine_special(self):
        special_prob = self.special_probs[self.day_tracker['current_day']]
        self.special = np.random.binomial(1, special_prob)

    def prep_for_next_day(self):
        self.headcount = 0
        self.determine_special()

    def increment_headcount(self):
        self.headcount += 1