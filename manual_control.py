#!/usr/bin/env python3

from __future__ import division, print_function

import sys
import numpy
import gym
import time
from optparse import OptionParser

from configurations import config_grabber as cg


try:
    import gym_minigrid
    from envelopes.mtsa.envelopes import *
except Exception as e:
    print(e)
    pass



def main():

    # logging.getLogger().setLevel(logging.INFO)

    observed = True

    cg.Configuration.set("training_mode", False)
    # cg.Configuration.set("debug_mode", False)

    parser = OptionParser()
    parser.add_option(
        "-e",
        "--env-name",
        dest="env_name",
        help="gym environment to load",
        default='MiniGrid-GoToObject-6x6-N2-v0'
    )
    (options, args) = parser.parse_args()


    # Getting configuration from file
    config = cg.Configuration.grab()

    # Overriding arguments with configuration file
    options.env_name = config.env_name


    # Load the gym environment
    env = gym.make(options.env_name)

    if config.envelope:
        env = SafetyEnvelope(env)


    def resetEnv():
        env.reset()
        if hasattr(env, 'mission'):
            print('Mission: %s' % env.mission)

    resetEnv()

    # Create a window to render into
    renderer = env.render('human')

    def keyDownCb(keyName):
        if keyName == 'BACKSPACE':
            resetEnv()
            return

        if keyName == 'ESCAPE':
            sys.exit(0)

        action = 0

        nonlocal observed

        if keyName == 'LEFT':
            action = env.actions.left
        elif keyName == 'RIGHT':
            action = env.actions.right
        elif keyName == 'UP':
            action = env.actions.forward

        elif keyName == 'SPACE':
            action = env.actions.toggle
        elif keyName == 'ALT':
            action = env.actions.clean
        elif keyName == 'PAGE_UP':
            action = env.actions.pickup
        elif keyName == 'PAGE_DOWN':
            action = env.actions.drop

        elif keyName == 'RETURN':
            action = env.actions.done

        else:
            print("unknown key %s" % keyName)
            return

        obs, reward, done, info = env.step(action)
        observed = True

        print('step=%s, reward=%.2f' % (env.step_count, reward))

        if done:
            print('done!')
            resetEnv()

    renderer.window.setKeyDownCb(keyDownCb)

    while True:
        env.render('human')
        time.sleep(0.01)
        if observed and config.envelope is True and config.envelope_type == "mtsa":
            env.step(-1)
            observed = False
        # If the window was closed
        if renderer.window == None:
            break

if __name__ == "__main__":
    main()
