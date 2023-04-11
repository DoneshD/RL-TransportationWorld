class Environment:
    def __init__(self):
        # Define a 3x3x3 matrix
        self.environment = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                            [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]
        self.mapping = {0: '-', 'D': 'D', 'P': 'P', 'R': 'R'}

    def delete_environment(self):
        self.environment = None

    def update_environment(self, x, y, z, value):
        self.environment[x][y][z] = value

    def get_cell(self, x, y, z):
        return self.mapping[self.environment[x][y][z]]

    def display_environment(self):
        for i in range(3):
            print(f"Level {i+1}:")
            for row in self.environment[i]:
                print([self.mapping[cell] for cell in row])
            print()


class Agent:
    def __init__(self, x, y, z, env):
        self.x = x
        self.y = y
        self.z = z
        self.env = env

    def ascend(self):
        if self.is_valid_move(self.x+1, self.y, self.z):
            self.x += 1
            return True
        return False

    def descend(self):
        if self.is_valid_move(self.x-1, self.y, self.z):
            self.x -= 1
            return True
        return False
    
    def move_right(self):
        if self.is_valid_move(self.x, self.y, self.z+1):
            self.z += 1
            return True
        return False

    def move_left(self):
        if self.is_valid_move(self.x, self.y, self.z-1):
            self.z -= 1
            return True
        return False

    def move_up(self):
        if self.is_valid_move(self.x, self.y-1, self.z):
            self.y -= 1
            return True
        return False

    def move_down(self):
        if self.is_valid_move(self.x, self.y+1, self.z):
            self.y += 1
            return True
        return False

    def is_valid_move(self, x, y, z):
        if x < 0 or x > 2 or y < 0 or y > 2 or z < 0 or z > 2:
            return False
        return True
    
    def get_AgentCell(self, x, y, z):
        return self.env.get_cell(x, y, z)
    
    def check_cell(agent, env):
        x, y, z = agent.x, agent.y, agent.z
        cell_value = env.get_cell(x, y, z)
        if cell_value == 'P':
            print("Pickup +10")
        elif cell_value == 'D':
            print("Dropoff +5")
        elif cell_value == 'R':
            print("Risky -10")
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
agent_env.environment = initial_env.environment.copy()  # make a copy of the initial environment
agent = Agent(0, 0, 0, agent_env)

# move the agent
agent.ascend()
agent.check_cell(initial_env)
agent.move_right()
agent.check_cell(initial_env)
agent.move_down()
agent.check_cell(initial_env)

initial_env.display_environment()


