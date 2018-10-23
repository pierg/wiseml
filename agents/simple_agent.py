import gym_minigrid
import gym

from envelopes.patterns.envelopes_light import  *
from stable_baselines.common.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.ppo2 import PPO2


env = gym.make('MiniGrid-DirtWatLightExp-9x9-v0')

env = SafetyEnvelope(env)

env = DummyVecEnv([lambda: env])  # The algorithms require a vectorized environment to run


model = PPO2(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=10000)

obs = env.reset()
for i in range(1000):
    action, _states = model.predict(obs)
    obs, rewards, dones, info = env.step(action)
    env.render()