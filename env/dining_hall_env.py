from env_utils import *
import numpy as np
import gymnasium as gym
from typing import List
from collections import namedtuple, deque

# DINING_HALL_OPENING_HOUR = 5
# DINING_HALL_CLOSING_HOUR = 10
# EATING_INTERVAL = .12  # 15 minutes


class Diner:
    def __init__(self, dining_time: int, dining_hall_count: int, day_tracker: dict):
        self.dining_time = dining_time
        self.dining_hall_count = dining_hall_count
        self.day_tracker = day_tracker
        self.prev_dining_hall = None

    def choose_dining_hall(self):
        dining_hall = int(np.floor(np.random.random() * self.dining_hall_count))
        self.prev_dining_hall = dining_hall
        return dining_hall


class DiningHall:
    def __init__(self, day_tracker: dict):
        self.headcount = 0
        self.day_tracker = day_tracker
        self.special_probs = np.random.rand(self.day_tracker['total_days'])
        self.determine_special()

    def determine_special(self):
        special_prob = self.special_probs[self.day_tracker['current_day']]
        self.special = np.random.choice(
            [0, 1], p=[1 - special_prob, special_prob])

    def prep_for_next_day(self):
        self.headcount = 0
        self.determine_special()

    def increment_headcount(self):
        self.headcount += 1


# class DiningManager:
#     def __init__(self, num_halls, day_tracker: dict):
#         self.day_tracker = day_tracker
#         self.num_halls = num_halls

#     def setup_diners(self, num_diners, num_dining_time_choices, dining_time_func):
#         self.diners = []
#         dining_times = dining_time_func(
#             num_diners, num_dining_time_choices).sort()
#         for dining_time in dining_times:
#             new_diner = Diner(dining_time, self.num_halls, self.day_tracker)
#             self.diners.append(new_diner)

#     def setup_halls(self):
#         self.dining_halls = []
#         for _ in range(self.num_halls):
#             new_hall = DiningHall(self.day_tracker)
#             self.dining_halls.append(new_hall)

#     def reset(self, start_day=0):
#         for dining_hall in self.dining_halls:
#             dining_hall.headcount = 0
#         self.day_tracker['current_day'] = start_day

#     def step(self):
#         assert self.diners and self.dining_halls
#         rewards = []
#         for diner in self.diners:
#             chosen_hall_idx = diner.choose_dining_hall()
#             self.dining_halls[chosen_hall_idx].increment_headcount()
#         self.day_tracker['current_day'] += 1
#         if self.day_tracker['current_day'] == self.day_tracker['total_days']:
#             # Done
#             pass
#         else:
#             for dining_hall in self.dining_halls:
#                 dining_hall.prep_for_next_day()
Transition = namedtuple("Transition", ("state", "action", "next_state", "reward"))

class ReplayBuffer:

    
    def __init__(self, capacity: int) -> None:
        self.memory = deque([], maxlen=capacity)
        
    def push(self, *args) -> None:
        """Save a transition"""
        self.memory.append(Transition(*args))
    def sample(self, batch_size) -> list[Transition]:
        return np.random.choice(self.memory, batch_size)

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
        self.num_diners = num_diners
        self.reward_function = reward_function

        self.setup_diners(num_diners, num_dining_times, dining_time_func)
        self.setup_halls()

    def setup_diners(self, num_diners, num_dining_time_choices, dining_time_func):
        dining_times = np.sort(dining_time_func(
            num_diners, num_dining_time_choices))
        print("DINING TIMES:")
        print(dining_times)
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
        return {'specials_vector': None, 'dining_times': self.dining_times, 'day': self.day_tracker['current_day']}

    # def _get_info(self):
    #     return {"info": {"eating_time": self._diner_eating_time, "eating_time_stringified": get_timestring(self._diner_eating_time)}}

    # def _get_reward(self, action: int, num_diners: int):
    #     received_special = np.random.binomial(
    #         self._special_probs[action, self._current_day], 1)
    #     return self._reward_function(num_diners, received_special=received_special)

    # def _populate_dining_halls(self):
    #     return self._populate_function(self._special_probs[:, self._current_day], self._num_other_diners)

    def reset(self, start_day=0, options=None):
        # this allows for new eating times upon first reset
        # self._diner_eating_time = (np.random.random(
        # ) * DINING_HALL_OPENING_HOUR) + (DINING_HALL_CLOSING_HOUR - DINING_HALL_OPENING_HOUR)
        # self._current_day = 0
        # observation = self._get_obs()
        # info = self._get_info()
        for dining_hall in self.dining_halls:
            dining_hall.headcount = 0
        self.day_tracker['current_day'] = start_day
        return self.get_obs()

    # def step(self, action: int):
    #     # as per environment spec, enables sequentiality
    #     assert action != self._prev_dining_hall
    #     # get special probabilities for today
    #     num_diners_in_dining_halls = self._populate_dining_halls()
    #     num_diners_in_specific_hall: np.ndarray = np.round(
    #         num_diners_in_dining_halls[action])
    #     reward = self._get_reward(action, num_diners_in_specific_hall)
    #     observation = self._get_obs()
    #     terminated = self._current_day + 1 == self._num_dining_days
    #     info = self._get_info()
    #     self._current_day = (self._current_day + 1) % self._num_dining_days
    #     return observation, reward, terminated, False, info

    def step(self):
        obs = self.get_obs()
        rewards = []
        done = None

        for diner in self.diners:
            chosen_hall_idx = diner.choose_dining_hall()
            chosen_hall = self.dining_halls[chosen_hall_idx]
            reward = self.reward_function(chosen_hall.headcount, chosen_hall.special)
            rewards.append(reward)
            self.dining_halls[chosen_hall_idx].increment_headcount()

        self.day_tracker['current_day'] += 1
        done = self.day_tracker['current_day'] == self.day_tracker['total_days']
        if not done:
            for dining_hall in self.dining_halls:
                dining_hall.prep_for_next_day()
        return obs, rewards, done

    def render(self):
        raise NotImplementedError

# observation should be (what day it is, )
