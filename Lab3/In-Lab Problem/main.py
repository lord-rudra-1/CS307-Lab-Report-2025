from functions.tabulate import tabulate
import heapq
from typing import List, Tuple, Optional

from functions.best_first_search import best_first_search
from functions.a_star import a_star_search

# Define the starting configuration of the puzzle
initial_board = [
    [2, 2, 1, 1, 1, 2, 2],
    [2, 2, 1, 1, 1, 2, 2],
    [1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 0, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1],
    [2, 2, 1, 1, 1, 2, 2],
    [2, 2, 1, 1, 1, 2, 2]
]

# Store results from all algorithm runs
results_table = []

# List of algorithms and heuristics to evaluate
algorithms_to_run = [
    ("Best First Search", best_first_search, "Manhattan"),
    ("Best First Search", best_first_search, "Exponential"),
    ("A* Search", a_star_search, "Manhattan"),
    ("A* Search", a_star_search, "Exponential")
]

# Execute each algorithm with the specified heuristic
for algo_name, algo_func, heuristic in algorithms_to_run:
    print(f"Running {algo_name} using {heuristic} heuristic")
    
    solution = algo_func(initial_board, heuristic)
    
    if solution:
        results_table.append([algo_name, heuristic, "Solution found", solution[0], solution[1]])
    else:
        results_table.append([algo_name, heuristic, "No solution found", "N/A", "N/A"])

# Display the results in a formatted table
print(tabulate(results_table, headers=["Algorithm", "Heuristic", "Result", "Path Length", "Explored Nodes"]))

