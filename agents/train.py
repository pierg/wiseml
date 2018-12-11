import gym_minigrid
import gym
import time

from stable_baselines.bench import Monitor

from configurations import config_grabber as cg
from configurations import args_grabber as ag

from stable_baselines.common.policies import MlpLstmPolicy
from stable_baselines.common.vec_env import SubprocVecEnv
from stable_baselines import PPO2

from agents.utils_functions import *

config = cg.Configuration.grab()
args = ag.get_args()

if args.n_timesteps != -1:
    cg.Configuration.set("n_timesteps", args.n_timesteps)

if args.env_name:
    cg.Configuration.set("env_name", args.env_name)

verbose = args.verbose * 1

env_id = config.env_name
n_timesteps = config.n_timesteps

n_cpu = 4
env = SubprocVecEnv([lambda: gym.make(env_id) for i in range(n_cpu)])

model = PPO2(MlpLstmPolicy, env, verbose=verbose, tensorboard_log="../evaluation/tensorboard/")
print("...starting the training for " + str(n_timesteps) + "...")
model.learn(total_timesteps=n_timesteps)
model_id = "PPO2_" + env_id + "_" + str(n_timesteps) + "ts"
model.save("./trained_models/" + model_id)

del model

print("Trained Finished!")
