import gym_minigrid
import gym
import time

from envelopes.patterns.envelopes_light import *
from stable_baselines.bench import Monitor

from stable_baselines.common.policies import MlpPolicy, MlpLstmPolicy, MlpLnLstmPolicy
from stable_baselines.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines import PPO2

from agents.utils_functions import *


env_id = "MiniGrid-LavaCrossingS9N1-v0"
env = SubprocVecEnv([lambda: gym.make(env_id) for i in range(n_cpu)])

model = PPO2.load("trained_models/MiniGrid")
print("Model Loaded!")

# Enjoy trained agent
obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()


