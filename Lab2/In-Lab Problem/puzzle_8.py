from collections import deque
import time
import math
import random

# -------------------- Node Representation --------------------
class PuzzleNode:
    """Represents a node in the search tree for the 8-puzzle problem."""
    def __init__(self, state, parent=None, depth=0):
        self.state = state
        self.parent = parent
        self.depth = depth  # Track depth for depth-limited search

# -------------------- Successor Generation --------------------
def generate_neighbors(node):
    """Generate valid neighboring states by sliding the blank tile (0)."""
    neighbors = []
    index = node.state.index(0)
    possible_moves = [-1, 1, -3, 3]  # Left, Right, Up, Down

    for move in possible_moves:
        new_index = index + move

        # Validate boundary conditions for 3x3 grid
        if 0 <= new_index < 9 and not (index % 3 == 0 and move == -1) and not (index % 3 == 2 and move == 1):
            new_state = list(node.state)
            new_state[index], new_state[new_index] = new_state[new_index], new_state[index]
            neighbors.append(PuzzleNode(new_state, node, node.depth + 1))
    
    return neighbors

# -------------------- Depth-Limited Search --------------------
def depth_limited_search(node, goal_state, limit):
    """Recursive depth-limited search (DLS)."""
    if node.state == goal_state:
        return node
    if node.depth == limit:
        return None

    for neighbor in generate_neighbors(node):
        result = depth_limited_search(neighbor, goal_state, limit)
        if result:
            return result
    return None

# -------------------- Iterative Deepening Search --------------------
def iterative_deepening_search(start_state, goal_state):
    """Run IDS by incrementally increasing the search depth."""
    depth = 0
    while True:
        print(f"Exploring depth limit: {depth}")
        result = depth_limited_search(PuzzleNode(start_state), goal_state, depth)
        if result:
            return result
        depth += 1

# -------------------- Backtrack Solution Path --------------------
def extract_solution_path(goal_node):
    """Reconstruct the path from start to goal node."""
    path = []
    current = goal_node
    while current:
        path.append(current.state)
        current = current.parent
    return list(reversed(path))

# -------------------- Random Goal State Generator --------------------
def create_random_goal_state(depth):
    """Create a randomized puzzle configuration by applying 'depth' random moves."""
    base_state = [1, 2, 3, 4, 5, 6, 7, 8, 0]
    current_node = PuzzleNode(base_state)
    for _ in range(depth):
        current_node = random.choice(generate_neighbors(current_node))
    return current_node.state

# -------------------- Test IDS on Multiple Depths --------------------
def run_ids_test_for_depth(depth):
    """Run IDS for a generated goal state of specified depth."""
    initial_state = [1, 2, 3, 4, 5, 6, 7, 0, 8]
    goal_state = create_random_goal_state(depth)
    print(f"\nGenerated goal state (depth {depth}): {goal_state}")

    start_time = time.time()
    result = iterative_deepening_search(initial_state, goal_state)
    
    if result:
        path = extract_solution_path(result)
        print("Solution path found:")
        for step in path:
            print(step)
        print(f"Steps in solution: {len(path)}")
    else:
        print("No solution could be found.")

    end_time = time.time()
    print(f"Execution time: {math.ceil((end_time - start_time) * 1000)} ms")

# -------------------- Run Tests --------------------
for d in [10, 20, 30, 40, 50, 100]:
    run_ids_test_for_depth(d)
