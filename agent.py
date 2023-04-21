import random
from pprint import pprint


class Agent:
    def __init__(self, x, y, z, env):
        self.x = x  # level
        self.y = y  # row
        self.z = z  # column
        self.env = env
        self.last_pos = None
        self.has_pickup = False
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
        if self.env.pickups[(self.x, self.y, self.z)] == 0:
            return -1
        self.has_pickup = True
        self.env.pickups[(self.x, self.y, self.z)] -= 1
        if self.env.pickups[(self.x, self.y, self.z)] == 0:
            self.env.update_environment(self.x, self.y, self.z, '-')
            del self.env.pickups[(self.x, self.y, self.z)]
        self.cumulativeReward += 14
        return 14

    def add_dropoff_reward(self):
        if self.env.dropoffs[(self.x, self.y, self.z)] == 0:
            return -1
        self.has_pickup = False
        self.env.dropoffs[(self.x, self.y, self.z)] -= 1
        if self.env.dropoffs[(self.x, self.y, self.z)] == 0:
            self.env.update_environment(self.x, self.y, self.z, '-')
            del self.env.dropoffs[(self.x, self.y, self.z)]
        self.cumulativeReward += 14
        return 14

    def remove_risk_reward(self):
        self.cumulativeReward -= 2
        return -2

    def ascend(self, env):
        if self.is_valid_move(self.x+1, self.y, self.z):
            self.last_pos = (self.x, self.y, self.z)
            self.x += 1
            self.last_action = 'ascend'
            self.check_cell(env)
            return True
        return False

    def descend(self, env):
        if self.is_valid_move(self.x-1, self.y, self.z):
            self.last_pos = (self.x, self.y, self.z)
            self.x -= 1
            self.last_action = 'descend'
            self.check_cell(env)
            return True
        return False

    def move_right(self, env):
        if self.is_valid_move(self.x, self.y, self.z+1):
            self.last_pos = (self.x, self.y, self.z)
            self.z += 1
            self.last_action = 'move_right'
            self.check_cell(env)
            return True
        return False

    def move_left(self, env):
        if self.is_valid_move(self.x, self.y, self.z-1):
            self.last_pos = (self.x, self.y, self.z)
            self.z -= 1
            self.last_action = 'move_left'
            self.check_cell(env)
            return True
        return False

    def move_up(self, env):
        if self.is_valid_move(self.x, self.y-1, self.z):
            self.last_pos = (self.x, self.y, self.z)
            self.y -= 1
            self.last_action = 'move_up'
            self.check_cell(env)
            return True
        return False

    def move_down(self, env):
        if self.is_valid_move(self.x, self.y+1, self.z):
            self.last_pos = (self.x, self.y, self.z)
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

    def update_q_learning_q_table(self, reward, alpha, gamma):
        print("----------------------Updating Qtable-------------------------------\n")
        pos = (self.x, self.y, self.z)
        old_value = self.Qtable[self.last_pos][self.last_action]
        next_max = max(self.Qtable[pos].values())
        new_value = ((1 - alpha) * old_value) + (alpha * (reward + (gamma * next_max)))
        self.Qtable[self.last_pos][self.last_action] = new_value
        print("Updating", new_value)
        print("----------------------Done Updating Qtable--------------------------\n")


    def check_cell(self, env):
        cell_value = env.get_cell(self.x, self.y, self.z)
        print("Cell value: ", cell_value)
        if cell_value == 'P':
            if self.has_pickup:
                print("Already has pickup")
                self.update_q_learning_q_table(-1, alpha=0.3, gamma=0.5)
                return

            print("Pickup +14")
            self.update_q_learning_q_table(self.add_pickkup_reward(), alpha=0.3, gamma=0.5)

        elif cell_value == 'D':
            if not self.has_pickup:
                print("No pickup")
                self.update_q_learning_q_table(-1, alpha=0.3, gamma=0.5)
                return

            print("Dropoff +14")
            self.update_q_learning_q_table(self.add_dropoff_reward(), alpha=0.3, gamma=0.5)

        elif cell_value == 'R':
            print("Risky -2")
            self.update_q_learning_q_table(self.remove_risk_reward(), alpha=0.3, gamma=0.5)

        else:
            self.update_q_learning_q_table(-1, alpha=0.3, gamma=0.5)
            print("Nothing")

    def q_learning(self, policy, learning_rate, discount_factor):
            print("Q-Learning")
            print("Policy:", policy)
            print("Initial state:", (self.x, self.y, self.z))
            print("Initial cumulativeReward", self.cumulativeReward)
            print("Initial agent environment:")
            pos = (self.x, self.y, self.z)
            self.env.display_environment(pos)
            for _ in range(500):
                pos = (self.x, self.y, self.z)
                if len(self.env.dropoffs) == 0:
                    return
                randomChoice = random.randint(0, 5)
                if randomChoice == 0:
                    print("Ascend")
                    self.ascend(self.env)
                elif randomChoice == 1:
                    print("Descend")
                    self.descend(self.env)
                elif randomChoice == 2:
                    print("Move up")
                    self.move_up(self.env)
                elif randomChoice == 3:
                    print("Move down")
                    self.move_down(self.env)
                elif randomChoice == 4:
                    print("Move left")
                    self.move_left(self.env)
                else:
                    print("Move right")
                    self.move_right(self.env)
            pprint(self.Qtable)
            print("Pickup blocks", self.env.pickups)
            print("Dropoff blocks", self.env.dropoffs)
            self.env.display_environment(pos)

            if policy == "Random":
                print("Do 9500 loops Random")
            elif policy == "Greedy":
                print("Do 9500 loops Greedy")
            elif policy == "Exploit":
                print("Do 9500 loops Exploit")
            else:
                print("Invalid policy")
            
        

    def sarsa(self, policy, learning_rate, discount_factor):
        print("SARSA")
        print("Policy:", policy)
        print("Initial state:", (self.x, self.y, self.z))
        print("Initial cumulativeReward", self.cumulativeReward)
        print("Initial agent environment:")
