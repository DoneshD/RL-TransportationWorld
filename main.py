import agent
import argparse
import environment

import numpy as np
import random

def main(algorithm=None, policy=None, lr=None, d=None):
    # create environment
    env = environment.Environment()

    # update the environment
    env.update_environment(0, 1, 1, 'P')
    env.update_environment(1, 0, 2, 'P')
    env.update_environment(0, 2, 2, 'D')
    env.update_environment(1, 2, 0, 'D')
    env.update_environment(2, 1, 2, 'D')
    env.update_environment(2, 2, 0, 'D')
    env.update_environment(0, 1, 2, 'R')
    env.update_environment(1, 1, 1, 'R')

    # create an agent
    agent_env = environment.Environment()
    agent_env.environment = env.environment.copy()
    agent_one = agent.Agent(0, 2, 0, agent_env)

    # check which algorithm to run
    if algorithm == 'Q-Learning' or algorithm == 'Q':
        agent_one.q_learning(policy, lr, d)
    elif algorithm == 'SARSA' or algorithm == 'S':
        agent_one.sarsa(policy, lr, d)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='UH COSC AI Final Project')
    parser.add_argument('-a', help='algorithm to run', metavar='algorithm',
                        required=True)
    parser.add_argument('-p', help='policy to run', metavar='policy',
                        required=True)
    parser.add_argument('-lr', help='learning rate', metavar='learning rate',
                        required=True)
    parser.add_argument('-d', help='discount rate', metavar='discount',
                        required=True)
    args = parser.parse_args()
    main(args.a, args.p)

    
