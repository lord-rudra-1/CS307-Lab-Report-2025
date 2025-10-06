from collections import deque

# -----------------------------
# Node Structure
# -----------------------------
class PuzzleNode:
    def __init__(self, configuration, parent=None, move=None):
        self.configuration = configuration  # Current state of the puzzle
        self.parent = parent                # Reference to the parent node
        self.move = move                    # Move that led to this state


# -----------------------------
# Generate all valid successors
# -----------------------------
def generate_successors(node):
    successors = []
    config = node.configuration
    empty_pos = config.index('O')  # Position of empty space
    valid_moves = []

    # Check possible single-step moves
    if empty_pos > 0 and config[empty_pos - 1] == 'E':
        valid_moves.append(empty_pos - 1)
    if empty_pos < 6 and config[empty_pos + 1] == 'W':
        valid_moves.append(empty_pos + 1)

    # Check possible jump moves
    if empty_pos > 1 and config[empty_pos - 2] == 'E':
        valid_moves.append(empty_pos - 2)
    if empty_pos < 5 and config[empty_pos + 2] == 'W':
        valid_moves.append(empty_pos + 2)

    # Generate new states based on valid moves
    for move in valid_moves:
        new_config = list(config)
        new_config[empty_pos], new_config[move] = new_config[move], new_config[empty_pos]
        successors.append(PuzzleNode(new_config, node, move))

    return successors


# -----------------------------
# Breadth-First Search (BFS)
# -----------------------------
def breadth_first_search(start_config, goal_config):
    start_node = PuzzleNode(start_config)
    goal_node = PuzzleNode(goal_config)
    frontier = deque([start_node])
    visited = set()
    max_frontier_size = 0
    nodes_explored = 0

    while frontier:
        node = frontier.popleft()

        if tuple(node.configuration) in visited:
            continue
        visited.add(tuple(node.configuration))
        nodes_explored += 1

        # Goal test
        if node.configuration == list(goal_node.configuration):
            path = []
            while node:
                path.append(node.configuration)
                node = node.parent
            print("Total nodes explored (BFS):", nodes_explored)
            print("Maximum queue size (BFS):", max_frontier_size)
            return path[::-1]

        # Expand successors
        for child in generate_successors(node):
            frontier.append(child)

        max_frontier_size = max(max_frontier_size, len(frontier))

    print("Total nodes explored (BFS):", nodes_explored)
    print("Maximum queue size (BFS):", max_frontier_size)
    return None


# -----------------------------
# Depth-First Search (DFS)
# -----------------------------
def depth_first_search(start_config, goal_config):
    start_node = PuzzleNode(start_config)
    goal_node = PuzzleNode(goal_config)
    stack = deque([start_node])
    visited = set()
    max_stack_size = 0
    nodes_explored = 0

    while stack:
        node = stack.pop()

        if tuple(node.configuration) in visited:
            continue
        visited.add(tuple(node.configuration))
        nodes_explored += 1

        # Goal test
        if node.configuration == list(goal_node.configuration):
            path = []
            while node:
                path.append(node.configuration)
                node = node.parent
            print("Total nodes explored (DFS):", nodes_explored)
            print("Maximum stack size (DFS):", max_stack_size)
            return path[::-1]

        # Expand successors
        for child in generate_successors(node):
            stack.append(child)

        max_stack_size = max(max_stack_size, len(stack))

    print("Total nodes explored (DFS):", nodes_explored)
    print("Maximum stack size (DFS):", max_stack_size)
    return None


# -----------------------------
# Main Execution
# -----------------------------
if __name__ == "__main__":
    initial_config = ('E', 'E', 'E', 'O', 'W', 'W', 'W')
    target_config = ('W', 'W', 'W', 'O', 'E', 'E', 'E')

    bfs_result = breadth_first_search(initial_config, target_config)
    if bfs_result:
        print("\nSolution path (BFS):")
        for step_no, config in enumerate(bfs_result, start=1):
            print(f"Step {step_no}: {config}")
        print("Total steps (BFS):", len(bfs_result))
    else:
        print("No solution found using BFS.")

    dfs_result = depth_first_search(initial_config, target_config)
    if dfs_result:
        print("\nSolution path (DFS):")
        for step_no, config in enumerate(dfs_result, start=1):
            print(f"Step {step_no}: {config}")
        print("Total steps (DFS):", len(dfs_result))
    else:
        print("No solution found using DFS.")

