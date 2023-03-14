from env.dining_hall_env import DiningHallEnv


env = DiningHallEnv(num_diners=10, num_dining_days=7, num_dining_halls=5)
state = env.reset()
