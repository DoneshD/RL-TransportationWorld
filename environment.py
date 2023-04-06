class Environment:
    def __init__(self):
        # Define a 3x3x3 matrix
        self.environment = [[[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                            [[0, 0, 0], [0, 0, 0], [0, 0, 0]],
                            [[0, 0, 0], [0, 0, 0], [0, 0, 0]]]

    def delete_environment(self):
        self.environment = None

    def update_environment(self, x, y, z, value):
        self.environment[x][y][z] = value

    def get_cell(self, x, y, z):
        return self.environment[x][y][z]

    def display_environment(self):
        for i in range(3):
            print(f"Level {i+1}:")
            for row in self.environment[i]:
                print(row)
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
        # if self.is_valid_move(self.x, self.y+1, self.z):
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
        if self.env.get_cell(x, y, z) == 'D':
            return False
        return True



# create an instance of the environment
env = Environment()

# update the environment
env.update_environment(0, 1, 1, 'P')
env.update_environment(1, 0, 2, 'P')
env.update_environment(0, 2, 2, 'D')
env.update_environment(1, 2, 0, 'D')
env.update_environment(2, 1, 2, 'D')
env.update_environment(2, 2, 0, 'D')
env.update_environment(0, 1, 2, 'R')
env.update_environment(1, 1, 1, 'R')

# create an instance of the agent
agent = Agent(0, 0, 0, env)
env.display_environment()

# moves it right
agent.ascend()
agent.move_right()
agent.move_down()

# display the updated environment with the agent's current position
env.update_environment(agent.x, agent.y, agent.z, 'A')
env.display_environment()



