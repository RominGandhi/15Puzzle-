import random

class Puzzle:
    def __init__(self, size):
        self.n = size  # size input for matrix n by n (4x4 for 15-puzzle)
        self.open = []
        self.closed = []

    def generate_random_state(self, moves=100):
        """Generate a random, reachable 15-puzzle state."""
        goal_state = [['1', '2', '3', '4'],
                      ['5', '6', '7', '8'],
                      ['9', '10', '11', '12'],
                      ['13', '14', '15', '_']]
        
        # Copy the goal state to avoid modifying the original
        state = [row[:] for row in goal_state]
        x, y = 3, 3  # Position of the blank space in the goal state

        # Define the possible moves: left, right, up, down
        moves_list = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for _ in range(moves):
            # Select a random move
            move = random.choice(moves_list)
            new_x, new_y = x + move[0], y + move[1]

            # Ensure the move is within the puzzle boundaries
            if 0 <= new_x < self.n and 0 <= new_y < self.n:
                # Swap the blank space with the adjacent tile
                state[x][y], state[new_x][new_y] = state[new_x][new_y], state[x][y]
                x, y = new_x, new_y

        return state

    def print_puzzle(self, state):
        """Utility function to print the current puzzle state."""
        for row in state:
            print(" ".join(row))
        print()

# Create a 4x4 Puzzle instance
puzzle = Puzzle(4)

# Generate 100 random states
random_states = []
for i in range(100):
    state = puzzle.generate_random_state(moves=50)
    random_states.append(state)
    print(f"Random State {i + 1}:")
    puzzle.print_puzzle(state)
