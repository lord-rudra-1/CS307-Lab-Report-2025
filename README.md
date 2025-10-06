# CS307 Lab Report 2025

This repository contains the solutions for the lab assignments in the CS307 course. Each lab folder contains an in-lab problem and a challenge problem.

## Lab 1: Uninformed Search

### In-Lab Problem: Missionary and Cannibal Problem

- **File:** `Lab1/In-Lab Problem/missionary_cannibal.py`
- **Description:** This file provides a generic Breadth-First Search (BFS) implementation. While named for the Missionary and Cannibal problem, the example implementation demonstrates a simple graph traversal.

### Challenge Problem: Rabbit Leap Puzzle

- **File:** `Lab1/Challenge Problem/rabbit_leap_problem.py`
- **Description:** This script solves the Rabbit Leap puzzle using both Breadth-First Search (BFS) and Depth-First Search (DFS). It finds the solution path and compares the number of nodes explored and the maximum size of the frontier/stack for each algorithm.

## Lab 2: Informed (Heuristic) Search

### In-Lab Problem: 8-Puzzle

- **File:** `Lab2/In-Lab Problem/puzzle_8.py`
- **Description:** Solves the 8-puzzle problem using Iterative Deepening Search (IDS). The script generates random goal states to test the algorithm's performance at various solution depths.

### Challenge Problem: A* Plagiarism Checker

- **File:** `Lab2/Challenge Problem/A_star_plag_checker.py`
- **Description:** An A*-based plagiarism detector. It uses A* search to align sentences between two documents based on the Levenshtein (edit) distance. It then identifies potentially plagiarized sentences by checking for low edit distances or high similarity scores.

## Lab 3: Local Search

### In-Lab Problem: 7x7 Puzzle with A* and Best-First Search

- **Files:** `Lab3/In-Lab Problem/main.py`, `Lab3/In-Lab Problem/functions/`
- **Description:** This program implements and compares Best-First Search and A* Search for solving a 7x7 puzzle. It evaluates two different heuristics: Manhattan distance and an "Exponential" heuristic, and tabulates the results.

### Challenge Problem: 3-SAT Solver

- **Files:** `Lab3/Challenge Problem/k_sat.py`, `Lab3/Challenge Problem/k_sat_unsat.py`
- **Description:** These scripts implement and compare several local search algorithms (Hill Climbing, Beam Search, Variable Neighborhood Descent) for solving the 3-Satisfiability (3-SAT) problem.
  - `k_sat.py`: Uses a clause weighting heuristic.
  - `k_sat_unsat.py`: Uses the number of unsatisfied clauses as the heuristic.

## Lab 4: Simulated Annealing

### In-Lab Problem: Traveling Salesperson Problem (TSP)

- **File:** `Lab4/In-Lab Problem/tsp_rajasthan_sa_problem.py`
- **Description:** Solves the Traveling Salesperson Problem (TSP) for a set of cities in Rajasthan using Simulated Annealing. The script experiments with different cooling rates (`alpha`) and visualizes the optimal tour found for each rate.

### Challenge Problem: Image Denoising

- **Files:** `Lab4/Challenge Problem/main.py`, `Lab4/Challenge Problem/functions/`
- **Description:** This program uses Simulated Annealing for image denoising. It takes a noisy image (`lena.txt`) and attempts to reconstruct the original image by minimizing the energy of the system.