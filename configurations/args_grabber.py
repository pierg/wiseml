import argparse

def get_args():
    parser = argparse.ArgumentParser(description='RL')
    parser.add_argument('--env_name', default=False,
                        help='environment to train on')
    parser.add_argument('--n_timesteps', type=int, default=-1,
                        help='number of timesteps to train the agent')


    args = parser.parse_args()

    return args
