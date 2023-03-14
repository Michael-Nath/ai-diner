from env.env_utils import *
from env.dining_hall import DiningHall
from env.diner import Diner
import numpy as np
import gymnasium as gym

# DINING_HALL_OPENING_HOUR = 5
# DINING_HALL_CLOSING_HOUR = 10
# EATING_INTERVAL = .12  # 15 minutes


class DiningHallEnv(gym.Env):
    def __init__(self,
                 num_diners,
                 num_dining_halls,
                 num_dining_times,
                 num_dining_days=7,
                 start_day=0,
                 dining_time_func=dining_times_random,
                 reward_function=reward_short_waits,
                 render_mode=None
                 ):
        # assert num_dining_days > 0 and num_dining_halls > 0
        self.num_halls = num_dining_halls
        self.day_tracker = {'current_day': start_day,
                            'total_days': num_dining_days}
        self.num_dining_days = num_dining_days
        self.num_diners = num_diners
        self.reward_function = reward_function
        self.setup_diners(num_diners, num_dining_times, dining_time_func)
        self.unvailable_halls = np.full(num_diners, -1)
        self.setup_halls()

    def setup_diners(self, num_diners, num_dining_time_choices, dining_time_func):
        dining_times = np.sort(dining_time_func(
            num_diners, num_dining_time_choices))
        print("DINING TIMES:")
        self.dining_times = dining_times
        
        self.diners = []
        for dining_time in dining_times:
            new_diner = Diner(dining_time, self.num_halls, self.day_tracker)
            self.diners.append(new_diner)

    def setup_halls(self):
        self.dining_halls = []
        for _ in range(self.num_halls):
            new_hall = DiningHall(self.day_tracker)
            self.dining_halls.append(new_hall)

    def get_obs(self):
        special_probs = np.array([dining_hall.special_probs for dining_hall in self.dining_halls])
        return {'day': self.day_tracker['current_day'], 'unavailable_halls': self.unvailable_halls, "special_probs":special_probs}

    def reset(self, start_day=0, options=None):
        for dining_hall in self.dining_halls:
            dining_hall.headcount = 0
        self.day_tracker['current_day'] = start_day
        return self.get_obs()

    def step(self, a):
        obs = self.get_obs()
        done = None
        step_reward = 0
        for idx, diner in enumerate(self.diners):
            assert a[idx] >= 0 and a[idx] < len(self.dining_halls)
            visited_hall_twice = diner.prev_dining_hall == a[idx]
            diner.visit_dining_hall(a[idx])
            chosen_hall = self.dining_halls[a[idx]]
            diner_reward = self.reward_function(chosen_hall.headcount, chosen_hall.special, visited_hall_twice)
            step_reward += diner_reward
            self.dining_halls[a[idx]].increment_headcount()

        self.day_tracker['current_day'] = (self.day_tracker['current_day'] + 1) % self.num_dining_days
        done = self.day_tracker['current_day'] == self.day_tracker['total_days']
        if not done:
            for dining_hall in self.dining_halls:
                dining_hall.prep_for_next_day()
        return obs, step_reward, done

    def render(self):
        raise NotImplementedError

# observation should be (what day it is, )
