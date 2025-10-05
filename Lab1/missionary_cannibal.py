from collections import deque

# Define a Node class to represent each state in the search
class Node:
    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent

# Function to get successors of a node (must be problem-specific)
def GetSuccessors(node):
    """
    This function should return a list of Node objects 
    that are reachable from the current node.
    Example:
        return [Node(next_state, node), ...]
    """
    # Placeholder — must be defined for your problem
    return []

def BFS(S, G):
    # Initialize start and goal nodes
    start_node = Node(S)
    goal_node = Node(G)

    # Initialize the queue and visited set
    queue = deque([start_node])
    visited = set()

    # Begin BFS loop
    while queue:
        node = queue.popleft()  # Dequeue front node

        # Skip if already visited
        if tuple(node.state) in visited:
            continue

        visited.add(tuple(node.state))

        # Check if goal is reached
        if node.state == goal_node.state:
            path = []
            while node is not None:
                path.append(node.state)
                node = node.parent
            return path[::-1]  # Return reversed path (start → goal)

        # Add all successors to queue
        for successor in GetSuccessors(node):
            queue.append(successor)

    # If goal not found
    return None


# Example usage (for a simple graph search)
if __name__ == "__main__":
    # Define a small example graph
    graph = {
        'A': ['B', 'C'],
        'B': ['D', 'E'],
        'C': ['F'],
        'D': [],
        'E': ['F'],
        'F': []
    }

    def GetSuccessors(node):
        successors = []
        for neighbor in graph.get(node.state, []):
            successors.append(Node(neighbor, node))
        return successors

    path = BFS('A', 'F')
    print("Path found:", path)
