import random

class Agent:
    def __init__(self, x, y, z, env):
        self.x = x  # level
        self.y = y  # row
        self.z = z  # column
        self.env = env
        self.pos = (x, y, z)
        self.cumulativeReward = 0

        self.Qtable = {}
        for x in range(3):
            for y in range(3):
                for z in range(3):
                    state = (x, y, z)
                    self.Qtable[state] = {}
                    for action in self.get_valid_actions(state):
                        self.Qtable[state][action] = 0.0

    def add_pickkup_reward(self):
        self.cumulativeReward += 10
        print("New cumulative reward", self.cumulativeReward)

    def add_dropoff_reward(self):
        self.cumulativeReward += 5
        print("New cumulative reward", self.cumulativeReward)

    def remove_risk_reward(self):
        self.cumulativeReward -= 10
        print("New cumulative reward:", self.cumulativeReward)

    def ascend(self, env):
        if self.is_valid_move(self.x+1, self.y, self.z):
            self.x += 1
            self.last_action = 'ascend'
            self.check_cell(env)
            return True
        return False

    def descend(self, env):
        if self.is_valid_move(self.x-1, self.y, self.z):
            self.x -= 1
            self.last_action = 'descend'
            self.check_cell(env)
            return True
        return False

    def move_right(self, env):
        if self.is_valid_move(self.x, self.y, self.z+1):
            self.z += 1
            self.last_action = 'move_right'
            self.check_cell(env)
            return True
        return False

    def move_left(self, env):
        if self.is_valid_move(self.x, self.y, self.z-1):
            self.z -= 1
            self.last_action = 'move_left'
            self.check_cell(env)
            return True
        return False

    def move_up(self, env):
        if self.is_valid_move(self.x, self.y-1, self.z):
            self.y -= 1
            self.last_action = 'move_up'
            self.check_cell(env)
            return True
        return False

    def move_down(self, env):
        if self.is_valid_move(self.x, self.y+1, self.z):
            self.y += 1
            self.last_action = 'move_down'
            self.check_cell(env)
            return True
        return False

    def is_valid_move(self, x, y, z):
        if x < 0 or x > 2 or y < 0 or y > 2 or z < 0 or z > 2:
            return False
        return True

    def get_state(self):
        return (self.x, self.y, self.z)

    def get_AgentCell(self, x, y, z):
        return self.env.get_cell(x, y, z)
    
    def get_valid_actions(self, state):
        actions = []
        if self.is_valid_move(state[0]+1, state[1], state[2]):
            actions.append('ascend')
        if self.is_valid_move(state[0]-1, state[1], state[2]):
            actions.append('descend')
        if self.is_valid_move(state[0], state[1], state[2]+1):
            actions.append('move_right')
        if self.is_valid_move(state[0], state[1], state[2]-1):
            actions.append('move_left')
        if self.is_valid_move(state[0], state[1]-1, state[2]):
            actions.append('move_up')
        if self.is_valid_move(state[0], state[1]+1, state[2]):
            actions.append('move_down')
        return actions
    
    def update_q_table(self, state, action, reward, next_state, alpha, gamma):
        # if state not in self.Qtable:
        #     self.Qtable[state] = {}
        if action not in self.Qtable[state]:
            self.Qtable[state][action] = 0.0
        old_value = self.Qtable[state][action]
        next_max = max(self.Qtable[next_state].values())
        new_value = (1 - alpha) * old_value + alpha * (reward + gamma * next_max)
        self.Qtable[state][action] = new_value
        print("Updating", new_value)

    
    def chooseReward(self):
        state = self.get_state()
        valid_actions = self.get_valid_actions(state)
        
        # Check if pickup and dropoff are applicable
        pickup_applicable = False
        dropoff_applicable = False
        for action in valid_actions:
            if action == 'P':
                pickup_applicable = True
            elif action == 'D':
                dropoff_applicable = True
        
        # Choose an applicable operator randomly
        if pickup_applicable and dropoff_applicable:
            action = random.choice(['P', 'D'])
        elif pickup_applicable:
            action = 'P'
        elif dropoff_applicable:
            action = 'D'
        else:
            action = random.choice(valid_actions)

    

    def check_cell(agent, env):
        x, y, z = agent.x, agent.y, agent.z
        cell_value = env.get_cell(x, y, z)
        print("Agent pos: ", (x, y, z))
        print("Cell value: ", cell_value)
        if cell_value == 'P':
            print("Pickup +10")
            agent.add_pickkup_reward()
            agent.update_q_table(agent.pos, agent.last_action, 10, agent.get_state(), alpha=0.3, gamma=0.5)
            env.update_environment(agent.x, agent.y, agent.z, '-')
            agent.env.update_environment(agent.x, agent.y, agent.z, '-')

        elif cell_value == 'D':
            print("Dropoff +5")
            agent.add_dropoff_reward()
            agent.update_q_table(agent.pos, agent.last_action, 5, agent.get_state(), alpha=0.3, gamma=0.5)
            env.update_environment(agent.x, agent.y, agent.z, '-')
            agent.env.update_environment(agent.x, agent.y, agent.z, '-')

        elif cell_value == 'R':
            print("Risky -10")
            agent.remove_risk_reward()
            agent.update_q_table(agent.pos, agent.last_action, -10, agent.get_state(), alpha=0.3, gamma=0.5)
            env.update_environment(agent.x, agent.y, agent.z, '-')
            agent.env.update_environment(agent.x, agent.y, agent.z, '-')
        else:
            print("Nothing")

    def q_learning(self, policy, learning_rate, discount_factor):
        
        if policy == "Random":
            print("Q-Learning")
            print("Policy:", policy)
            print("Initial state:", (self.x, self.y, self.z))
            print("Initial cumulativeReward", self.cumulativeReward)
            print("Initial agent environment:")
            self.env.display_environment(self.pos)
            for _ in range(10000):
                self.chooseReward()
                randomChoice = random.randint(0, 5)
                if randomChoice == 0:
                    self.ascend(self.env)
                elif randomChoice == 1:
                    self.descend(self.env)
                elif randomChoice == 2:
                    self.move_up(self.env)
                elif randomChoice == 3:
                    self.move_down(self.env)
                elif randomChoice == 4:
                    self.move_left(self.env)
                else:
                    self.move_right(self.env)
            print(self.Qtable)
            self.env.display_environment(self.pos)
        else:
            print("Invalid policy")

        if policy == "Exploit":
            print("Q-Learning")
            print("Policy:", policy)
            print("Initial state:", (self.x, self.y, self.z))
            print("Initial cumulativeReward", self.cumulativeReward)
            print("Initial agent environment:")
            self.env.display_environment(self.pos)
            for _ in range(500):
                self.chooseReward()
                randomChoice = random.randint(0, 5)
                if randomChoice == 0:
                    self.ascend(self.env)
                elif randomChoice == 1:
                    self.descend(self.env)
                elif randomChoice == 2:
                    self.move_up(self.env)
                elif randomChoice == 3:
                    self.move_down(self.env)
                elif randomChoice == 4:
                    self.move_left(self.env)
                else:
                    self.move_right(self.env)
            print(self.Qtable)
            self.env.display_environment(self.pos)
        else:
            print("Invalid policy")

        if policy == "Greedy":
            print("Q-Learning")
            print("Policy:", policy)
            print("Initial state:", (self.x, self.y, self.z))
            print("Initial cumulativeReward", self.cumulativeReward)
            print("Initial agent environment:")
            self.env.display_environment(self.pos)
            for _ in range(500):
                self.chooseReward()
                randomChoice = random.randint(0, 5)
                if randomChoice == 0:
                    self.ascend(self.env)
                elif randomChoice == 1:
                    self.descend(self.env)
                elif randomChoice == 2:
                    self.move_up(self.env)
                elif randomChoice == 3:
                    self.move_down(self.env)
                elif randomChoice == 4:
                    self.move_left(self.env)
                else:
                    self.move_right(self.env)
            print(self.Qtable)
            self.env.display_environment(self.pos)
        else:
            print("Invalid policy")
            
            

            

    def sarsa(self, policy, learning_rate, discount_factor):
        print("SARSA")
        print("Policy:", policy)
        print("Initial state:", (self.x, self.y, self.z))
        print("Initial cumulativeReward", self.cumulativeReward)
        print("Initial agent environment:")
        self.env.display_environment(self.pos)
