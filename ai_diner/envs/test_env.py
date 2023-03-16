from dining_hall_env import DiningHallEnv

# should be able to reset the environment

env = DiningHallEnv(5, 5, 10)
# observation, info = env.reset()
# observation, reward, terminated, truncated, info = env.step()
for _ in range(7):
    observation, reward, terminated = env.step()
    print(observation)
    print(reward)
    print(terminated)

