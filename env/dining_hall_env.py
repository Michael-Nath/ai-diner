from env_utils import *
import numpy as np
import gymnasium as gym


DINING_HALL_OPENING_HOUR = 5
DINING_HALL_CLOSING_HOUR = 10
EATING_INTERVAL = .12 # 15 minutes
class DiningHallEnv(gym.Env):
    def __init__(self, 
                 render_mode=None,
                 num_dining_halls=5, 
                 num_dining_days=7, 
                 num_other_diners=700,
                 populate_function=populate_proportionately,
                 reward_function=reward_short_waits
                 ):
        assert num_dining_days > 0
        assert num_dining_halls > 0
        self._num_dining_halls = num_dining_halls
        self._num_dining_days = num_dining_days
        self._num_other_diners = num_other_diners
        self._populate_function = populate_function
        self._reward_function = reward_function
        # normalize across rows (aka across the dining halls per day)
        self._special_probs = np.random.rand(self._num_dining_halls, self._num_dining_days)
        self._special_probs = self._special_probs / self._special_probs.sum(axis=0)
        self._prev_dining_hall = -1 # dining halls are numbered [0, {num_dining_halls - 1}]
        self._diner_eating_time = -1 # eating times should be between OPENING and CLOSING hour
        self._current_day = -1 # current day should be in range [0, {num_dining_days - 1}] 
    def _get_obs(self):
        return {"day": self._current_day}
    def _get_info(self):
        return {"info": {"eating_time": self._diner_eating_time, "eating_time_stringified": get_timestring(self._diner_eating_time)}} 
    def _get_reward(self, action: int, num_diners: int):
        received_special = np.random.binomial(self._special_probs[action, self._current_day], 1)
        return self._reward_function(num_diners, received_special=received_special)
    def _populate_dining_halls(self):
        return self._populate_function(self._special_probs[:, self._current_day], self._num_other_diners)
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        # this allows for new eating times upon first reset
        np.random.seed(seed)
        self._diner_eating_time = (np.random.random() * DINING_HALL_OPENING_HOUR) + (DINING_HALL_CLOSING_HOUR - DINING_HALL_OPENING_HOUR)
        self._current_day = int(np.random.random() * self._num_dining_days)
        observation = self._get_obs()
        info = self._get_info()
        return observation, info
    def step(self, action: int):
        assert action != self._prev_dining_hall # as per environment spec, enables sequentiality
        # get special probabilities for today
        num_diners_in_dining_halls = self._populate_dining_halls()
        num_diners_in_specific_hall: np.ndarray = np.round(num_diners_in_dining_halls[action])
        reward = self._get_reward(action, num_diners_in_specific_hall)
        observation = self._get_obs()
        terminated = self._current_day + 1 == self._num_dining_days
        info = self._get_info()
        self._current_day = (self._current_day + 1) % self._num_dining_days
        return observation, reward, terminated, False, info
    def render(self):
        raise NotImplementedError
    
# observation should be (what day it is, )