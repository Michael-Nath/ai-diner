from dining_hall_env import DiningHallEnv

# should be able to reset the environment

env = DiningHallEnv()
observation, info = env.reset()
observation, reward, terminated, truncated, info = env.step(1)
print(observation)
print(reward)
print(terminated)
print(truncated)
print(info)