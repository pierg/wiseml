import gym_minigrid
import gym
import time

from envelopes.patterns.envelopes_light import *
from stable_baselines.bench import Monitor

from configurations import config_grabber as cg

from stable_baselines.common.policies import MlpPolicy, MlpLstmPolicy, MlpLnLstmPolicy
from stable_baselines.common.vec_env import DummyVecEnv, SubprocVecEnv
from stable_baselines import PPO2

from agents.utils_functions import *

config = cg.Configuration.grab()



# Create log dir
log_dir = "./log_multi/"
os.makedirs(log_dir, exist_ok=True)

env_id = config.env_name
n_timesteps = config.max_num_steps

# multiprocess environment
n_cpu = config.n_cpu
env = SubprocVecEnv([lambda: gym.make(env_id) for i in range(n_cpu)])
# env = SubprocVecEnv([make_env(env_id, i, 0, log_dir) for i in range(n_cpu)])


model = PPO2(MlpLstmPolicy, env, verbose=1, tensorboard_log="./tensorboard/")
model.learn(total_timesteps=10000000000, callback=callback)
model.save("trained_models/MiniGrid")

del model # remove to demonstrate saving and loading

print("Trained Finished!")

model = PPO2.load("trained_models/MiniGrid")

# Enjoy trained agent
obs = env.reset()
while True:
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()


