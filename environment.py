class Environment:
    def __init__(self):
        # Define a 3x3x3 matrix
        self.environment = [[['-' for _ in range(3)] for _ in range(3)]
                            for _ in range(3)]

    def delete_environment(self):
        self.environment = None

    def update_environment(self, x, y, z, value):
        self.environment[x][y][z] = value

    def get_cell(self, x, y, z):
        return self.environment[x][y][z]

    def display_environment(self, agent_pos=None):
        for i, level in enumerate(self.environment):
            print(f"Level {i+1}:")
            for j, row in enumerate(level):
                display_row = []
                for k, cell in enumerate(row):
                    if agent_pos and i == agent_pos[0] and j == agent_pos[1] and k == agent_pos[2]:
                        display_row.append('A')
                    else:
                        display_row.append(cell)
                print(display_row)
            print()


class Agent:
    def __init__(self, x, y, z, env):
        self.x = x  # level
        self.y = y  # row
        self.z = z  # column
        self.env = env
        self.cumulativeReward = 0

    def add_pickkup_reward(self):
        self.cumulativeReward += 10
        print("New cumulative reward", self.cumulativeReward)

    def add_dropoff_reward(self):
        self.cumulativeReward += 5
        print("New cumulative reward", self.cumulativeReward)

    def remove_risk_reward(self):
        self.cumulativeReward -= 10
        print("New cumulative reward:", self.cumulativeReward)

    def ascend(self):
        if self.is_valid_move(self.x+1, self.y, self.z):
            self.x += 1
            self.check_cell(initial_env)
            return True
        return False

    def descend(self):
        if self.is_valid_move(self.x-1, self.y, self.z):
            self.x -= 1
            self.check_cell(initial_env)
            return True
        return False

    def move_right(self):
        if self.is_valid_move(self.x, self.y, self.z+1):
            self.z += 1
            self.check_cell(initial_env)
            return True
        return False

    def move_left(self):
        if self.is_valid_move(self.x, self.y, self.z-1):
            self.z -= 1
            self.check_cell(initial_env)
            return True
        return False

    def move_up(self):
        if self.is_valid_move(self.x, self.y-1, self.z):
            self.y -= 1
            self.check_cell(initial_env)
            return True
        return False

    def move_down(self):
        if self.is_valid_move(self.x, self.y+1, self.z):
            self.y += 1
            self.check_cell(initial_env)
            return True
        return False

    def is_valid_move(self, x, y, z):
        if x < 0 or x > 2 or y < 0 or y > 2 or z < 0 or z > 2:
            print("ERROR: Invalid move")
            return False
        return True

    def get_AgentCell(self, x, y, z):
        return self.env.get_cell(x, y, z)

    def check_cell(agent, env):
        x, y, z = agent.x, agent.y, agent.z
        cell_value = env.get_cell(x, y, z)
        print("Agent pos: ", (x, y, z))
        print("Cell value: ", cell_value)
        if cell_value == 'P':
            print("Pickup +10")
            agent.add_pickkup_reward()
            initial_env.update_environment(agent.x, agent.y, agent.z, '-')
            agent.env.update_environment(agent.x, agent.y, agent.z, '-')

        elif cell_value == 'D':
            print("Dropoff +5")
            agent.add_dropoff_reward()
            initial_env.update_environment(agent.x, agent.y, agent.z, '-')
            agent.env.update_environment(agent.x, agent.y, agent.z, '-')

        elif cell_value == 'R':
            print("Risky -10")
            agent.remove_risk_reward()
            initial_env.update_environment(agent.x, agent.y, agent.z, '-')
            agent.env.update_environment(agent.x, agent.y, agent.z, '-')
        else:
            print("Nothing")


# create an instance of the environment
initial_env = Environment()

# update the environment
initial_env.update_environment(0, 1, 1, 'P')
initial_env.update_environment(1, 0, 2, 'P')
initial_env.update_environment(0, 2, 2, 'D')
initial_env.update_environment(1, 2, 0, 'D')
initial_env.update_environment(2, 1, 2, 'D')
initial_env.update_environment(2, 2, 0, 'D')
initial_env.update_environment(0, 1, 2, 'R')
initial_env.update_environment(1, 1, 1, 'R')

# create an instance of the agent
agent_env = Environment()

# make a copy of the initial environment
agent_env.environment = initial_env.environment.copy()
agent = Agent(0, 2, 0, agent_env)

print("Initial Environment: \n")
initial_env.display_environment()

agent_pos = (agent.x, agent.y, agent.z)
print("Agent pos", agent_pos)

print("Initial Agent Environment: \n")
agent.env.display_environment(agent_pos)
# move the agent


agent.move_down()

print("New Environment: \n")
initial_env.display_environment()

agent_pos = (agent.z, agent.x, agent.y)
print("New Agent Environment: \n")
agent.env.display_environment(agent_pos)