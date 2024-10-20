import random

print("Enter the initial state matrix\nExample: 1 2 3 4\n5 6 7 8\n9 10 11 12\n13 14 15 _")

class Node:
    def __init__(self, data, level, fvalue):
        # Initialize node with a matrix (data), level (depth), and f-value (A* evaluation)
        self.data = data
        self.level = level
        self.fvalue = fvalue

    # Locate the position of the blank space ('_')
    def locate(self, puzzle, x):
        for i in range(0, len(self.data)):
            for k in range(0, len(self.data)):
                if puzzle[i][k] == x:
                    return i, k

    # Move the blank space with an adjacent tile, creating a new puzzle state
    def shuffle(self, puzzle, x1, y1, x2, y2):
        if 0 <= x2 < len(self.data) and 0 <= y2 < len(self.data[0]):
            temp_puzzle = self.copy(puzzle)  # Create a copy of the puzzle
            temp_puzzle[x2][y2], temp_puzzle[x1][y1] = temp_puzzle[x1][y1], temp_puzzle[x2][y2]  # Swap
            return temp_puzzle
        return None

    # Create subnodes by moving the blank space in four directions (left, right, up, down)
    def subnode(self):
        # Locate the current position of the blank space ('_')
        x, y = self.locate(self.data, '_')
        
        # Define potential moves for the blank space: left, right, up, down
        positions = [
            [x, y - 1],  # Move left
            [x, y + 1],  # Move right
            [x - 1, y],  # Move up
            [x + 1, y]   # Move down
        ]

        subnodes = []
        # Iterate over each potential move and create a subnode if the move is valid
        for new_x, new_y in positions:
            # Ensure that the new position is within the boundaries of the matrix (0 to size-1)
            if 0 <= new_x < len(self.data) and 0 <= new_y < len(self.data[0]):
                # Attempt to shuffle the blank space and create a new subnode
                node1 = self.shuffle(self.data, x, y, new_x, new_y)
                if node1 is not None:
                    # Create a new Node with the updated puzzle state
                    node2 = Node(node1, self.level + 1, 0)
                    subnodes.append(node2)

        return subnodes  # Return the list of generated subnodes


    # Create a deep copy of the puzzle matrix
    def copy(self, root):
        return [list(row) for row in root]


class Puzzle:
    def __init__(self, size):
        self.n = size  # Size of the puzzle grid (e.g., 4 for a 4x4 grid)
        self.heuristic = ''  # Choose heuristic: 'h1' for Misplaced Tiles, 'h2' for Manhattan Distance
        self.open = []
        self.closed = []
        self.nodes_expanded = 0  # Counter for nodes expanded
        self.steps_taken = 0 #counter for steps taken

    def action(self, heuristic, start, goal):
        self.heuristic = heuristic
        start = Node(start, 0, 0)  # Create a Node for the initial state
        start.fvalue = self.f(start, goal)  # Calculate the f-value for the start node
        self.open.append(start)  # Add the start node to the open list
        self.nodes_expanded = 0  # Reset nodes expanded counter
        self.steps_taken = 0 # reset steps taken counter

        print("\n\n")
        while True:
            current = self.open[0]  # Get the first node in the open list (node with smallest f-value)
            print("Next Matrix\n\n")
            for i in current.data:  # Print the current puzzle state
                    for k in i:
                        print(k, end=" ")
                    print("")

            if self.h(current.data, goal) == 0:  # If the current state matches the goal state
                print("Goal reached!")
                print(f"Total nodes expanded: {self.nodes_expanded}")
                print(f"Total steps taken to solve: {current.level}")
                self.steps_taken = current.level
                break

            # Generate and evaluate subnodes (neighboring states)
            for i in current.subnode():
                i.fvalue = self.f(i, goal)  # Calculate the f-value for each subnode
                self.open.append(i)
                self.nodes_expanded += 1  # Increment nodes expanded counter

            self.closed.append(current)  # Add the current node to the closed list
            del self.open[0]  # Remove the current node from the open list
            self.open.sort(key=lambda x: x.fvalue)  # Sort the open list by f-value (ascending order)

    def f(self, start, goal):
        # Calculate the f-value: f(x) = g(x) + h(x)
        return self.h(start.data, goal) + start.level

    def h(self, start, goal):
        # Choose the appropriate heuristic based on the user's choice ('h1' or 'h2')
        if self.heuristic == 'h1':
            return self.heuristic_misplaced_tiles(start, goal)
        elif self.heuristic == 'h2':
            return self.heuristic_manhattan_distance(start, goal)
        else:
            raise ValueError("Invalid heuristic selected")

    def heuristic_misplaced_tiles(self, start, goal):
        """ Heuristic h1: Counts the number of misplaced tiles """
        misplaced = 0
        for i in range(self.n):
            for j in range(self.n):
                if start[i][j] != goal[i][j] and start[i][j] != "_":
                    misplaced += 1
        return misplaced

    def heuristic_manhattan_distance(self, start, goal):
        """ Heuristic h2: Calculates the Manhattan distance """
        distance = 0
        goal_positions = {goal[i][j]: (i, j) for i in range(self.n) for j in range(self.n)}
        for i in range(self.n):
            for j in range(self.n):
                if start[i][j] != "_" and start[i][j] in goal_positions:
                    x_goal, y_goal = goal_positions[start[i][j]]
                    distance += abs(i - x_goal) + abs(j - y_goal)
        return distance
    
    def generate_random_state(self, moves):
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

results = []

# 4x4 matrix for 15-puzzle with heuristic selection
for i in range(100):
    start_state = Puzzle(4).generate_random_state(moves=30)
    goal_state = [['1', '2', '3', '4'],
                  ['5', '6', '7', '8'],
                  ['9', '10', '11', '12'],
                  ['13', '14', '15', '_']]  # Fixed goal state
    
    puzzle_h1 = Puzzle(4)
    puzzle_h1.action(heuristic='h1', start=start_state, goal=goal_state)
    
    # Store results for h1
    result_h1 = {
        "test_case": i + 1,
        "heuristic": 'h1',
        "steps_taken": puzzle_h1.steps_taken,
        "nodes_expanded": puzzle_h1.nodes_expanded
    }
    
    puzzle_h2 = Puzzle(4)  # Create a new puzzle instance for h2
    puzzle_h2.action(heuristic='h2', start=start_state, goal=goal_state)

    # Store results for h2
    result_h2 = {
        "test_case": i + 1,
        "heuristic": 'h2',
        "steps_taken": puzzle_h2.steps_taken,
        "nodes_expanded": puzzle_h2.nodes_expanded
    }

    results.append({
        "test_case": i + 1,
        "h1_steps_taken": result_h1['steps_taken'],
        "h1_nodes_expanded": result_h1['nodes_expanded'],
        "h2_steps_taken": result_h2['steps_taken'],
        "h2_nodes_expanded": result_h2['nodes_expanded']
    })
    


print("\nResults:")
print(f"{'Reachable Case':<10} | {'h1 Steps':<10} | {'h1 Nodes':<12} | {'h2 Steps':<10} | {'h2 Nodes':<12}")
print("-" * 62)
for result in results:
    print(f"{result['test_case']:<10} | {result['h1_steps_taken']:<10} | {result['h1_nodes_expanded']:<12} | {result['h2_steps_taken']:<10} | {result['h2_nodes_expanded']:<12}")

#need to do 100 times
#fix it taking long for some matrix
#need to put data in table
#need to do each for each heuristic, not selecing 1

#problems
#all step counts are the same
#nodes expanded are different
#h1 sometimes skips moves or goes diagonally or just does something weird