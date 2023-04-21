# greedy and exploit working for q-learning

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


    def perform_operation(self, string):
        if string == "move_right":
            print("move right")
            self.move_right(self.env)
        elif string == "move_left":
            print("move left")
            self.move_left(self.env)
        elif string == "move_up":
            print("move up")
            self.move_up(self.env)
        elif string == "move_down":
            print("move down")
            self.move_down(self.env)
        elif string == "ascend":
            print("ascend")
            self.ascend(self.env)
        elif string == "descend":
            print("descend")
            self.descend(self.env)


    # given the name of the operation in string form, perform the operation
    def perform_operation(self, string):
        if string == "move_right":
            print("move right")
            self.move_right(self.env)
        elif string == "move_left":
            print("move left")
            self.move_left(self.env)
        elif string == "move_up":
            print("move up")
            self.move_up(self.env)
        elif string == "move_down":
            print("move down")
            self.move_down(self.env)
        elif string == "ascend":
            print("ascend")
            self.ascend(self.env)
        elif string == "descend":
            print("descend")
            self.descend(self.env)

    # check if pickup or dropoff is available
    def pickup_or_dropoff_avail(self, env, next):
        cell_value = self.env.get_cell(next[0],next[1],next[2])

        if cell_value == 'P':
            if not self.has_pickup:
                print("\n")
                print(self.env.get_cell(next[0],next[1],next[2]))
                print(self.env.pickups[(next[0], next[1], next[2])])
                print("\n")
                return True
        elif cell_value == 'D':
            if self.has_pickup:
                print("\n")
                print(self.env.get_cell(next[0],next[1],next[2]))
                print(self.env.dropoffs[(next[0], next[1], next[2])])
                print("\n")
                return True
        else:
            return False
    
    # Greedy Policy - break ties by rolling a dice for operators with the same utility
    def greedy_tie_break(self,action_q_value_pair):
        print(action_q_value_pair)
        action_q_value_pair.sort(key=lambda x: x[1], reverse=True)
        index = 0
        print(action_q_value_pair)
        if len(action_q_value_pair) > 1:
            if action_q_value_pair[0][1] == action_q_value_pair[1][1]:
                last_tie_index = 1
                while last_tie_index < len(action_q_value_pair) and action_q_value_pair[last_tie_index][1] == action_q_value_pair[0][1]:
                    last_tie_index += 1
                    index = random.randint(0, last_tie_index)
        
        print(action_q_value_pair[index][0],action_q_value_pair[index][1])
        action_str = action_q_value_pair[index][0]
        self.perform_operation(action_str)

    # Exploit policy - break ties by rolling a dice for operators with the same utility,
    # 85% chance of choosing utility with tied q-value,
    # 15% chance of choosing utility with non-tied q-value
    def exploit_tie_break(self,action_q_value_pair):
        print(action_q_value_pair)
        action_q_value_pair.sort(key=lambda x: x[1], reverse=True)
        index = 0
        print(action_q_value_pair)
        if len(action_q_value_pair) > 1:
            if action_q_value_pair[0][1] == action_q_value_pair[1][1]:
                last_tie_index = 1
                while last_tie_index < len(action_q_value_pair) and action_q_value_pair[last_tie_index][1] == action_q_value_pair[0][1]:
                    last_tie_index += 1
                    tie_index = random.randint(0, last_tie_index)
                different_index = random.randint(tie_index+1, len(action_q_value_pair)-1)
                prob_dist = [0.85, 0.15]
                index = random.choices([tie_index, different_index], weights=prob_dist, k=2)

        print(action_q_value_pair[index][0],action_q_value_pair[index][1])
        action_str = action_q_value_pair[index][0]
        self.perform_operation(action_str)

    # executed when policy is either +Greedy" or "Explot"
    # if pickup or dropoff is applicable, choose operator, otherwise sort q-values
    # splits at tie breaking for the respective policies
    def greedy_exploit_part_1(self, policy, alpha = 0.3, gamma = 0.5):
        current_state = (self.get_state()[0],self.get_state()[1],self.get_state()[2])
        print("current: ", current_state)
        action_q_value_pair = []
        for action in self.get_valid_actions(self.get_state()):
            if action == "move_right":
                print("move_right",next_state)
                next_state = (self.get_state()[0],self.get_state()[1],self.get_state()[2]+1)
                if self.pickup_or_dropoff_avail(self.env,next_state) == True:
                    self.move_right(self.env)
                    return
    
            elif action == "move_left":
                next_state = (self.get_state()[0],self.get_state()[1],self.get_state()[2]-1)
                print("move_left",next_state)
                if self.pickup_or_dropoff_avail(self.env,next_state) == True:
                    self.move_left(self.env)
                    return
                
            
            elif action == "descend":
                next_state = (self.get_state()[0]-1,self.get_state()[1],self.get_state()[2])
                print("descend",next_state)
                if self.pickup_or_dropoff_avail(self.env,next_state) == True:
                    self.descend(self.env)
                    return

            elif action == "ascend":
                next_state = (self.get_state()[0]+1,self.get_state()[1],self.get_state()[2])
                print("ascend",next_state)
                if self.pickup_or_dropoff_avail(self.env,next_state) == True:
                    self.ascend(self.env)
                    return

            elif action == "move_up":
                next_state = (self.get_state()[0],self.get_state()[1]-1,self.get_state()[2])
                print("move_up",next_state)
                if self.pickup_or_dropoff_avail(self.env,next_state) == True:
                    self.move_up(self.env)
                    return

            else:
                next_state = (self.get_state()[0],self.get_state()[1]+1,self.get_state()[2])
                print("move_down",next_state)
                if self.pickup_or_dropoff_avail(self.env,next_state) == True:
                    self.move_down(self.env)
                    return

            # if reached this point then pick and dropoff was not available, calculate Q value for operator and add to list
            old_value = self.Qtable[self.get_state()][action]
            print(old_value)
            print(self.get_state())
            print(next_state)
            next_max = max(self.Qtable[next_state].values())
            print(next_max)
            cell_value = self.env.get_cell(next_state[0], next_state[1], next_state[2])
            if(cell_value == 'R'):
                new_value = ((1 - alpha) * old_value) + (alpha * (-2 + (gamma * next_max)))
            else:
                new_value = ((1 - alpha) * old_value) + (alpha * (-1 + (gamma * next_max)))
            action_q_value_pair.append([action,new_value])

        if policy == "Greedy":
            self.greedy_tie_break(action_q_value_pair)
        if policy == "Exploit":
            self.exploit_tie_break(action_q_value_pair)


    
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
                    pprint(self.Qtable)
                    print("Pickup blocks", self.env.pickups)
                    print("Dropoff blocks", self.env.dropoffs)
                    self.env.display_environment(pos)
                    print("Ended before")
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
            print("Ended first 500")

            if policy == "Random":
                print("Do 9500 loops Random")


            elif policy == "Greedy":
                for _ in range(9500):
                    pos = (self.x, self.y, self.z)
                    if len(self.env.dropoffs) == 0:
                        #pprint(self.Qtable)
                        print("Pickup blocks", self.env.pickups)
                        print("Dropoff blocks", self.env.dropoffs)
                        self.env.display_environment(pos)
                        print("Greedy - Ended before")
                        return
                    #pprint(self.Qtable)

                    print("Pickup blocks", self.env.pickups)
                    print("Dropoff blocks", self.env.dropoffs)
                    print("Greedy Prog")
                    self.env.display_environment(pos)
                    self.greedy_exploit_part_1(policy)

            elif policy == "Exploit":
                for _ in range(9500):
                    pos = (self.x, self.y, self.z)
                    if len(self.env.dropoffs) == 0:
                        #pprint(self.Qtable)
                        print("Pickup blocks", self.env.pickups)
                        print("Dropoff blocks", self.env.dropoffs)
                        self.env.display_environment(pos)
                        print("Exploit - Ended before")
                        return
                    #pprint(self.Qtable)
                    print("Pickup blocks", self.env.pickups)
                    print("Dropoff blocks", self.env.dropoffs)
                    print("Greedy Prog")
                    self.env.display_environment(pos)
                    self.greedy_exploit_part_1(policy)
            else:
                print("Invalid policy")
            
        

    def sarsa(self, policy, learning_rate, discount_factor):
        print("SARSA")
        print("Policy:", policy)
        print("Initial state:", (self.x, self.y, self.z))
        print("Initial cumulativeReward", self.cumulativeReward)
        print("Initial agent environment:")

