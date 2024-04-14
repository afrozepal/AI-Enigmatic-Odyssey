import copy

class Node:
    def __init__(self, grid=None, value=None):
        self.grid = grid
        self.children = []
        self.parent = None
        self.value = value
        self.depth=0

    def add_child(self, child_node):
        self.children.append(child_node)

def non_zero_indices(grid):
    indices = []
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] != 0:
                indices.append((i, j))
    return indices

def eating_cookies(grid2, r, c):
    for i in range(0, r + 1):
        for j in range(c, len(grid2[0])):
            grid2[i][j] = 0
    return grid2


def is_terminal(grid):
    for i in range(0,len(grid)):
        for j in range(0,len(grid[0])):
            if grid[i][j]!=0:
                return False
    return True


from collections import deque

def print_tree_bfs(root):
    if root is None:
        return

    queue = deque([(root, 0)])  # Initialize the queue with root node and its depth
    while queue:
        node, depth = queue.popleft()  # Dequeue a node and its depth
        print("Depth:", depth,"Parent:", node.parent.grid if node.parent else None, "Value:", node.value)
        for row in node.grid:
            print(row)
        print()  # Print an empty line after each grid representation

        # Enqueue children along with their depths
        for child in node.children:
            queue.append((child, depth + 1))

def assign_values(root):
    if root is None:
        return

    queue = deque([(root, 0)])  # Initialize the queue with root node and its depth

    while queue:
        node, depth = queue.popleft()  # Dequeue a node and its depth

        if depth % 2 == 0:  # Check if depth is even
            if not node.children:  # Check if node is terminal
                if node.grid:  # Check if the grid is not empty
                    node.value = 1
                else:
                    node.value = -1
        else:
            if not node.children:  # Check if node is terminal
                node.value = -1

        # Enqueue children along with their depths
        for child in node.children:
            queue.append((child, depth + 1))

def delete_tree(node):
    if not node:
        return
    
    for child in node.children:
        delete_tree(child)
    
    del node

def set_depth(node, depth=0):
    node.depth = depth
    for child in node.children:
        set_depth(child, depth + 1)

def back_track(node,depth):
        if not node:
            return []

        if not node.children:
            # Leaf node reached, backtrack
            parent_X=node.parent
            ##if any child has value none , first assign it value according to its child , 
            child_values = [child.value if child.value is not None else child.children[0].value for child in parent_X.children if child.value is not None or (child.children and child.children[0].value is not None)]
            if depth%2==0:
                parent_X.value=max(child_values)
            else:
                parent_X.value=min(child_values)
            
        for child in node.children:
            back_track(child, depth + 1)

###revised backtrack to resolve issues 
def back_track2(node,depth):
        if not node:
            return []

        if not node.children:
            # Leaf node reached, backtrack
            parent_X=node.parent
            ##if any child has value none , first assign it value according to its child , 
            child_values = [child.value for child in parent_X.children if child.value is not None]
            if depth%2==0:
            
                parent_X.value=max(child_values)
            else:
                parent_X.value=min(child_values)
            
        for child in node.children:
            back_track2(child, depth + 1)

def making_grid():
    row = input("Enter number of rows: ")
    col = input("Enter number of columns: ")
    row = int(row)
    col = int(col)
    grid = [[1 for _ in range(col)] for _ in range(row)]
    grid[row - 1][0] = 2
    for i in range(row):
        print(grid[i])  # to print one row at once
    return grid

def player_move(grid):
    print("Player's turn:")
    r = int(input("Enter row: (from 0 to {}): ".format(len(grid) - 1)))
    c = int(input("Enter column: (from 0 to {}): ".format(len(grid[0]) - 1)))

    if 0 <= r < len(grid) and 0 <= c < len(grid[0]):
        if grid[r][c] == 0:
            print("That cell is already eaten. Please choose another.")
            return player_move(grid)
        return r, c
    else:
        # Input values are out of range
        print("Input values are out of range.")
        return player_move(grid)
    
    
def tree_check(grid):
    root = Node(grid)
    current_g = copy.deepcopy(grid)
    queue = deque([(root, current_g)])  # Initialize the queue with root node and its grid
    i = 1
    while queue and i <= 7:
        level_size = len(queue)
        for _ in range(level_size):
            node, grid = queue.popleft()  # Dequeue a node and its grid
            
            # Generate children and enqueue them
            indices = non_zero_indices(grid)
            for index in indices:
                r, c = index
                grid2 = copy.deepcopy(grid)
                grid2 = eating_cookies(grid2, r, c)
                child_node = Node(grid2)
                node.add_child(child_node)
                child_node.parent=node
                queue.append((child_node, grid2))

        # Move to the next level
        i += 1

    # Assign values to nodes
    assign_values(root)
    set_depth(root)
    back_track(root ,-1)
    # Print the tree
    back_track2(root ,-1)
   # print_tree_bfs(root)

   #get best move 
    max_child_value = float('-inf')  # Initialize with negative infinity
    max_child_grid = None
    for child in root.children:
        if child.value is not None and child.value > max_child_value:
            max_child_value = child.value
            max_child_grid = child.grid

    print("AI move : ")
    for row in max_child_grid:
        print(row)
    print()

    delete_tree(root)
    return max_child_grid

def main():
    grid = making_grid()
    status=2
    key_value=input("enter 1 for first Human Move else other key for AI ")
    key_value=int(key_value)
    if(key_value==1):
        while not is_terminal(grid):
            player_r, player_c = player_move(grid)
            grid = eating_cookies(grid, player_r, player_c)
            print("The PLAYER MOVE is : ")
            for i in range(len(grid)):
                print(grid[i])  # to print one row at once
            status=1
            if not is_terminal(grid):
                ai_move=tree_check(grid)
                grid=ai_move
                status=2
    else:
        while not is_terminal(grid):
            ai_move=tree_check(grid)
            grid=ai_move
            status=2
            if not is_terminal(grid):
                player_r, player_c = player_move(grid)
                grid = eating_cookies(grid, player_r, player_c)
                print("The PLAYER MOVE is : ")
                for i in range(len(grid)):
                    print(grid[i])  # to print one row at once
                status=1

    print("Game Over")
    if status==1:
        print("Player 1 loose")
    else:
        print("Player 1 WINS")
    
main()
