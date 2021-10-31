import argparse

# import torch


def get_args():
    parser = argparse.ArgumentParser(description='RL')
    parser.add_argument(
        '--num-stacks',
        type=int,
        default=4)
    parser.add_argument(
        '--num-steps',
        type=int,
        default=100)
    parser.add_argument(
        '--test-steps',
        type=int,
        default=2000)
    parser.add_argument(
        '--num-frames',
        type=int,
        default=100000)

    ## other parameter
    parser.add_argument(
        '--log-interval',
        type=int,
        default=10,
        help='log interval, one log per n updates (default: 10)')
    parser.add_argument(
        '--save-img',
        type=bool,
        default=True)
    parser.add_argument(
        '--save-interval',
        type=int,
        default=10,
        help='save interval, one eval per n updates (default: None)')
    ##Q-learning参数
    parser.add_argument(
        '--learning-rate',
        type=float,
        default=0.01,
        help='Q-learning‘s learning rate'
    )
    parser.add_argument(
        '--discount-factor',
        type=float,
        default=0.9,
        help='Q-learning‘s discount factor'
    )
    parser.add_argument(
        '--greedy-epsilon',
        type=float,
        default=0.1,
        help='Q-learning‘s greedy epsilon'
    )
    args = parser.parse_args()


    return args