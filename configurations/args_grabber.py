import argparse

def get_args():
    parser = argparse.ArgumentParser(description='RL')
    parser.add_argument('--env_name', default=False,
                        help='environment to train on')
    parser.add_argument('--n_timesteps', type=int, default=-1,
                        help='number of timesteps to train the agent')
    parser.add_argument('--verbose', action='store_true', default=False,
                        help='set no monitor')
    parser.add_argument('--config_file_name', default=False,
                        help='configuration file name')


    args = parser.parse_args()

    return args
