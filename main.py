import agent
import argparse
import environment


def main(algorithm=None, policy=None):
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
    agent_env.pickups = env.pickups.copy()
    agent_env.dropoffs = env.dropoffs.copy()
    

    # check which algorithm to run
    if algorithm == 'Q-Learning' or algorithm == 'Q':
        agent_one = agent.Agent(0, 2, 0, agent_env, True)
        agent_one.TransformationWorld(policy)
    elif algorithm == 'SARSA' or algorithm == 'S':
        agent_one = agent.Agent(0, 2, 0, agent_env, False)
        agent_one.TransformationWorld(policy)
    else:
        print("Input valid parameters")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='UH COSC AI Final Project')
    parser.add_argument('-a', help='algorithm to run', metavar='algorithm',
                        required=True)
    parser.add_argument('-p', help='policy to run', metavar='policy',
                        required=True)
    args = parser.parse_args()
    main(args.a, args.p)

    