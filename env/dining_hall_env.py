import gymnasium as gym

class DiningHallEnv(gym.Env):
    def __init__(self, render_mode=None):
        raise NotImplementedError
    def _get_obs(self):
        raise NotImplementedError
    def _get_info(self):
        raise NotImplementedError
    def reset(self, seed=None, options=None):
        super().reset(seed=seed)
        raise NotImplementedError
    def step(self, action):
        raise NotImplementedError
    def render(self):
        raise NotImplementedError
    