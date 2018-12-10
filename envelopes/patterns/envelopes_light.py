
from configurations import config_grabber as cg

from extendedminigrid import *
from envelopes.perception import Perception

import gym



class SafetyEnvelope(gym.core.Wrapper):
    """
    Safety envelope for safe exploration.
    Uses monitors for avoiding unsafe actions and shaping rewards
    """

    def __init__(self, env):
        super(SafetyEnvelope, self).__init__(env)

        # Grab configuration
        self.config = cg.Configuration.grab()

        # Action proposed by the agent
        self.propsed_action = None

        # Action proposed by the monitor
        self.shaped_action = None

        # List of all monitors with their states, rewards and unsafe-actions
        self.meta_monitor = []

        # Dictionary that gets populated with information by all the monitors at runtime
        self.monitor_states = {}

        # Perceptions of the agent, it gets updated at each step with the current observations
        self.perception = Perception(env.gen_obs_decoded())

        # Set rewards
        self.step_reward = self.config.rewards.standard.step
        self.goal_reward = self.config.rewards.standard.goal
        self.death_reward = self.config.rewards.standard.death


    def which_action(self, action_planner):
        if action_planner == "wait":
            return self.env.actions.done
        elif action_planner == "turn_right":
            return self.env.actions.right
        elif action_planner == "toggle":
            return self.env.actions.toggle

    def step(self, proposed_action):

        if self.config.debug_mode:
            print("proposed_action = " + self.env.action_to_string(proposed_action))

        # Updating the perceptions from raw observations
        self.perception.update(self.env.gen_obs_decoded())

        # Rendering
        if self.config.rendering:
            self.env.render('human')

        n_violations = 0
        shaped_reward = 0
        safe_action = proposed_action

        if hasattr(self.config, 'monitors'):
            if hasattr(self.config.monitors, 'patterns'):
                for pattern in self.config.monitors.patterns:
                    for rule in pattern:
                        if rule.type == "absence":
                            if self.perception.is_condition_satisfied(rule.conditions, proposed_action):
                                if self.config.debug_mode:
                                    print("violation detected: " + rule.name)
                                n_violations += 1
                                shaped_reward += rule.rewards.violated
                                if rule.mode == "enforcing":
                                    safe_action = self.which_action(rule.action_planner)
                            else:
                                shaped_reward += rule.rewards.respected

                        if rule.type == "universality":
                            if not self.perception.is_condition_satisfied(rule.conditions, proposed_action):
                                if self.config.debug_mode:
                                    print("violation detected: " + rule.name)
                                n_violations += 1
                                shaped_reward += rule.rewards.violated
                                if rule.mode == "enforcing":
                                    safe_action = self.which_action(rule.action_planner)
                            else:
                                shaped_reward += rule.rewards.respected

                        if rule.type == "precedence":
                            if (self.perception.is_condition_satisfied(rule.conditions.post, proposed_action)
                                    and not self.perception.is_condition_satisfied(rule.conditions.pre)):
                                if self.config.debug_mode:
                                    print("violation detected: " + rule.name)
                                n_violations += 1
                                shaped_reward += rule.rewards.violated
                                if rule.mode == "enforcing":
                                    safe_action = self.which_action(rule.action_planner)
                            else:
                                shaped_reward += rule.rewards.respected

                        if rule.type == "response":
                            if (self.perception.is_condition_satisfied(rule.conditions.pre)
                                    and not self.perception.is_condition_satisfied(rule.conditions.post, proposed_action)):
                                if self.config.debug_mode:
                                    print("violation detected: " + rule.name)
                                n_violations += 1
                                shaped_reward += rule.rewards.violated
                                if rule.mode == "enforcing":
                                    safe_action = self.which_action(rule.action_planner)
                            else:
                                shaped_reward += rule.rewards.respected

        # Send a suitable action to the environment
        obs, reward, done, info = self.env.step(safe_action)

        # Shape the reward at the cumulative sum of all the rewards from the monitors
        reward += shaped_reward

        for i in range(n_violations):
            info["event"].append("violation")


        return obs, reward, done, info