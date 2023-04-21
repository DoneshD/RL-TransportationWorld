class Environment:
    def __init__(self):
        # Define a 3x3x3 matrix
        self.environment = [[['-' for _ in range(3)] for _ in range(3)]
                            for _ in range(3)]
        self.pickups = dict()
        self.dropoffs = dict()

    def delete_environment(self):
        self.environment = None

    def update_environment(self, x, y, z, value):
        self.environment[x][y][z] = value
        if value == 'P':
            self.pickups[(x, y, z)] = 10
        elif value == 'D':
            self.dropoffs[(x, y, z)] = 5

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
