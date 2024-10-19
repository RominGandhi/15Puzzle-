print("Enter the initial state matrix\nExample: 1 2 3 4\n5 6 7 8\n9 10 11 12\n13 14 15 _")
class Node:
    def __init__(self, data, level, fvalue):
        # initialize node 
        self.data = data
        self.level = level
        self.fvalue = fvalue

    # locate where the blank space is
    def locate(self, puzzle, x): 
        for i in range(0, len(self.data)):
            for k in range(0, len(self.data)):
                if puzzle[i][k] == x:
                    return i, k
                
    # move the blank space in the direction tasked
    def shuffle(self, puzzle, x1, y1, x2, y2): 
        # check if position is in bounds
        if 0 <= x2 < len(self.data) and 0 <= y2 < len(self.data[0]):
            temp_puzzle = []
            temp_puzzle = self.copy(puzzle)  # create copy
            temp = temp_puzzle[x2][y2]
            temp_puzzle[x2][y2] = temp_puzzle[x1][y1]
            temp_puzzle[x1][y1] = temp
            return temp_puzzle
        else:
            return None

    # create subnodes from given node by moving blank space
    def subnode(self):
        # four directions: left, right, up, down
        x, y = self.locate(self.data, '_')
        positions = [[x, y - 1], [x, y + 1], [x - 1, y], [x + 1, y]]
        subnodes = []
        for i in positions:
            node1 = self.shuffle(self.data, x, y, i[0], i[1])
            if node1 is not None:
                node2 = Node(node1, self.level + 1, 0)
                subnodes.append(node2)
        return subnodes  # return subnode list

    # creates a deepcopy of the matrix as a list of lists
    def copy(self, root):
        temp = []
        for i in root:
            temp.append(list(i))
        return temp


class Puzzle:
    def __init__(self, size):
        self.n = size  # size input for matrix n by n (4x4 for 15-puzzle)
        self.open = []
        self.closed = []

    def action(self):
        # input the first and last matrix
        print("Enter the initial matrix (has one blank space as '_'):\n\nExample:\n1 2 3 4\n5 6 7 8\n9 10 11 12\n13 14 15 _\n")
        start = self.obtain()
        print("Enter the goal state matrix:\n")
        goal = self.obtain()
        start = Node(start, 0, 0)
        start.fvalue = self.f(start, goal)
        self.open.append(start)
        print("\n\n")
        while True:
            current = self.open[0]
            print("Next Matrix\n\n")
            for i in current.data:
                for k in i:
                    print(k, end=" ")
                print("")
            for i in current.subnode():
                i.fvalue = self.f(i, goal)
                self.open.append(i)
            self.closed.append(current)
            del self.open[0]
            if self.h(current.data, goal) == 0:
                print("Goal reached!")
                break
            self.open.sort(key=lambda x: x.fvalue, reverse=False)

    def obtain(self):
        puzzle = []
        for i in range(0, self.n):
            temp = input().split(" ")
            puzzle.append(temp)
        return puzzle

    def f(self, start, goal):
        return self.h(start.data, goal) + start.level

    def h(self, start, goal):
        temp = 0
        for i in range(0, self.n):
            for k in range(0, self.n):
                if start[i][k] != goal[i][k] and start[i][k] != "_":
                    temp += 1
        return temp


# 4x4 matrix for 15-puzzle
print("Welcome to the 15-Puzzle!\n\nAn initial matrix will be shuffled into the goal matrix.\n")
puzzle = Puzzle(4)
puzzle.action()
