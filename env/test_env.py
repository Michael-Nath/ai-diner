from dining_hall_env import DiningHallEnv

# should be able to reset the environment

env = DiningHallEnv()
observation, info = env.reset()
print(observation)
print(info)