import gym_minigrid
import gym
import time

from stable_baselines.bench import Monitor

from stable_baselines import logger
from stable_baselines.bench import Monitor
from stable_baselines.common import set_global_seeds
from stable_baselines.common.cmd_util import make_atari_env

from stable_baselines.common.vec_env import DummyVecEnv
from configurations import config_grabber as cg
from configurations import args_grabber as ag

from stable_baselines.common.policies import MlpLstmPolicy
from stable_baselines.common.vec_env import SubprocVecEnv
from stable_baselines import PPO2

from agents.utils_functions import *

import random, string


args = ag.get_args()

if args.n_timesteps != -1:
    print("...setting up the n_timesteps to " + str(args.n_timesteps) + "...")
    cg.Configuration.set("n_timesteps", args.n_timesteps)

if args.env_name:
    cg.Configuration.set("env_name", args.env_name)

verbose = args.verbose * 1

# Create log dir
log_dir = "../evaluation/"
os.makedirs(log_dir, exist_ok=True)

config = cg.Configuration.grab()

env_id = config.env_name
random_id = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(4))

n_timesteps = config.n_timesteps
n_cpu = config.n_cpu
algo = eval(config.algo)
policy = eval(config.policy)
config_name = config.config_custom_name + "_" + config.algo + "_" + config.policy + "_ts" + str(config.n_timesteps) + "_ncpu" + str(n_cpu) + "__" + str(random_id)
cg.Configuration.set("config_name", config_name)
log_dir_config = log_dir + config_name + "/"
os.makedirs(log_dir_config, exist_ok=True)
shutil.copy("../configurations/main.json", log_dir_config)



def make_env(env_id, rank, seed=0):
    """
    Utility function for multiprocessed env.

    :param env_id: (str) the environment ID
    :param num_env: (int) the number of environments you wish to have in subprocesses
    :param seed: (int) the inital seed for RNG
    :param rank: (int) index of the subprocess
    """

    def _init():
        env = gym.make(env_id)
        env.seed(seed + rank)
        env = Monitor(env, log_dir_config + str(rank), allow_early_resets=True)
        return env

    set_global_seeds(seed)
    return _init

def callback(_locals, _globals):
  """
  Callback called at each step (for DQN an others) or after n steps (see ACER or PPO2)
  :param _locals: (dict)
  :param _globals: (dict)
  """
  global n_steps, best_mean_reward
  # Print stats every 1000 calls
  if (n_steps + 1) % 10 == 0:
      # Evaluate policy performance
      x, y = ts2xy(load_results(log_dir_config), 'timesteps')
      if len(x) > 0:
          mean_reward = np.mean(y[-100:])
          print(x[-1], 'timesteps')
          print("Best mean reward: {:.2f} - Last mean reward per episode: {:.2f}".format(best_mean_reward, mean_reward))

          # New best model, you could save the agent here
          if mean_reward > best_mean_reward:
              best_mean_reward = mean_reward
              # Example for saving best model
              print("Saving new best model")
              _locals['self'].save(log_dir_config + "_timestep_" + str(n_steps))
  n_steps += 1
  return True

# Create the vectorized environment
env = SubprocVecEnv([make_env(env_id, i) for i in range(n_cpu)])

# env = SubprocVecEnv([lambda: gym.make(env_id) for i in range(n_cpu)])

model = algo(policy, env, verbose=verbose, tensorboard_log="../evaluation/tensorboard/")
print("...starting the training for " + str(n_timesteps) + "...")
model.learn(total_timesteps=n_timesteps, callback=callback, tb_log_name=config_name)
model.save("./trained_models/" + config_name)

del model

print("Trained Finished!")
