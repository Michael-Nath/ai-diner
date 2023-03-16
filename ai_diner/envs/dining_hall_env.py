from ai_diner.envs.env_utils import *
from ai_diner.envs.dining_hall import DiningHall
from ai_diner.envs.diner import Diner
import numpy as np
# import gymnasium as gym
import gym

# DINING_HALL_OPENING_HOUR = 5
# DINING_HALL_CLOSING_HOUR = 10
# EATING_INTERVAL = .12  # 15 minutes


class DiningHallEnv(gym.Env):
    def __init__(self,
                 num_diners = 10,
                 num_dining_halls = 5,
                 num_dining_times = 4,
                 num_dining_days=7,
                 dining_time_func=dining_times_random,
                 reward_function=reward_short_waits,
                 render_mode=None
                 ):
        super(DiningHallEnv, self).__init__()
        self.action_space = gym.spaces.MultiDiscrete(np.full(num_diners, num_dining_halls))
        self.observation_space = gym.spaces.Dict(
            {
                "current_day": gym.spaces.Discrete(num_dining_days),
                "unavailable_halls": gym.spaces.MultiDiscrete(np.full(num_diners, num_dining_halls + 1))
             }
            )
        # assert num_dining_days > 0 and num_dining_halls > 0
        self.num_halls = num_dining_halls
        self.day_tracker = {'current_day': np.random.randint(0, num_dining_days),
                            'total_days': num_dining_days}
        self.num_dining_days = num_dining_days
        self.num_diners = num_diners
        self.reward_function = reward_function
        self.setup_diners(num_diners, num_dining_times, dining_time_func)
        self.unvailable_halls = np.random.randint(0, num_dining_halls, num_diners)
        self.setup_halls()
        self.special_probs = np.array([dining_hall.special_probs for dining_hall in self.dining_halls])

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
        return {'current_day': self.day_tracker['current_day'], 'unavailable_halls': self.unvailable_halls}

    def reset(self, start_day=0, options=None):
        for dining_hall in self.dining_halls:
            dining_hall.headcount = 0
        self.day_tracker['current_day'] = start_day
        return self.get_obs()

    def step(self, a):
        done = None
        step_reward = 0
        for idx, diner in enumerate(self.diners):
            assert a[idx] >= 0 and a[idx] < len(self.dining_halls)
            visited_hall_twice = diner.prev_dining_hall == (a[idx])
            diner.visit_dining_hall(a[idx])
            chosen_hall = self.dining_halls[a[idx]]
            diner_reward = self.reward_function(chosen_hall.headcount, chosen_hall.special, visited_hall_twice)
            self.unvailable_halls[idx] = a[idx]
            step_reward += diner_reward
            self.dining_halls[a[idx]].increment_headcount()

        self.day_tracker['current_day'] = (self.day_tracker['current_day'] + 1) % self.num_dining_days
        done = self.day_tracker['current_day'] == self.day_tracker['total_days']
        if not done:
            for dining_hall in self.dining_halls:
                dining_hall.prep_for_next_day()
        info = {"special_probs": self.special_probs}
        obs = self.get_obs()
        return obs, step_reward, done, info

    def render(self):
        raise NotImplementedError

# observation should be (what day it is, )
