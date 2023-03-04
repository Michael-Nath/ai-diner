from env_utils import *
import numpy as np
import gymnasium as gym


DINING_HALL_OPENING_HOUR = 5
DINING_HALL_CLOSING_HOUR = 10
EATING_INTERVAL = .12 # 15 minutes
class DiningHallEnv(gym.Env):
    def __init__(self, render_mode=None, num_dining_halls=5, num_dining_days=7):
        assert num_dining_days > 0
        assert num_dining_halls > 0
        self._special_probabilities = np.random.rand(num_dining_halls, num_dining_days)
        self._num_dining_halls = num_dining_halls
        self._num_dining_days = num_dining_days
        # normalize across rows (aka across the dining halls per day)
        self._special_probabilities = self._special_probabilities / self._special_probabilities.sum(axis=0)
        self._prev_dining_hall = -1 # dining halls are numbered [0, {num_dining_halls - 1}]
        self._diner_eating_time = -1 # eating times should be between OPENING and CLOSING hour
        self._current_day = -1 # current day should be in range [0, {num_dining_days - 1}] 
    def _get_obs(self):
        return {"day": self._current_day}
    def _get_info(self):
        return {"info": {"eating_time": self._diner_eating_time, "eating_time_stringified": get_timestring(self._diner_eating_time)}} 
    def _get_reward(self):
        raise NotImplementedError
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        # this allows for new eating times upon first reset
        np.random.seed(seed)
        self._diner_eating_time = (np.random.random() * DINING_HALL_OPENING_HOUR) + (DINING_HALL_CLOSING_HOUR - DINING_HALL_OPENING_HOUR)
        self._current_day = int(np.random.random() * self._num_dining_days)
        observation = self._get_obs()
        info = self._get_info()
        return observation, info
    def step(self, action):
        assert action != self._prev_dining_hall # as per environment spec, enables sequentiality
        
        raise NotImplementedError
    def render(self):
        raise NotImplementedError
    
# observation should be (what day it is, )