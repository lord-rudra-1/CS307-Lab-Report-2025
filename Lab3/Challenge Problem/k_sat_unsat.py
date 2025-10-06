import random

# ------------------------------------------------------------
# Generate a Random 3-SAT Problem
# ------------------------------------------------------------
def generate_3sat_instance(num_vars, num_clauses):
    """Creates a random 3-SAT problem with given number of variables and clauses."""
    sat_instance = []
    for _ in range(num_clauses):
        clause_vars = random.sample(range(1, num_vars + 1), 3)
        clause = [v if random.choice([True, False]) else -v for v in clause_vars]
        sat_instance.append(clause)
    return sat_instance


# ------------------------------------------------------------
# Evaluate the Number of Unsatisfied Clauses
# ------------------------------------------------------------
def count_unsatisfied_clauses(clauses, solution):
    """Counts how many clauses are unsatisfied under the current solution."""
    unsatisfied_count = 0
    for clause in clauses:
        satisfied = any(
            (literal > 0 and solution[literal - 1]) or
            (literal < 0 and not solution[-literal - 1])
            for literal in clause
        )
        if not satisfied:
            unsatisfied_count += 1
    return unsatisfied_count


# ------------------------------------------------------------
# Hill Climbing based on Unsatisfied Clauses
# ------------------------------------------------------------
def hill_climb_unsat(clauses, num_vars, max_steps=1000):
    """Performs hill climbing to minimize unsatisfied clauses."""
    solution = [random.choice([True, False]) for _ in range(num_vars)]
    for _ in range(max_steps):
        current_unsat = count_unsatisfied_clauses(clauses, solution)
        if current_unsat == 0:
            return solution, True  # Found a valid solution

        best_flip = None
        best_unsat = current_unsat

        for var_idx in range(num_vars):
            solution[var_idx] = not solution[var_idx]
            new_unsat = count_unsatisfied_clauses(clauses, solution)
            if new_unsat < best_unsat:
                best_unsat = new_unsat
                best_flip = var_idx
            solution[var_idx] = not solution[var_idx]  # revert change

        if best_flip is None:
            break  # No improvement
        solution[best_flip] = not solution[best_flip]  # commit the best move

    return solution, False


# ------------------------------------------------------------
# Beam Search based on Unsatisfied Clauses
# ------------------------------------------------------------
def beam_search_unsat(clauses, num_vars, beam_width=3, max_steps=1000):
    """Performs beam search using unsatisfied clauses heuristic."""
    beam = [[random.choice([True, False]) for _ in range(num_vars)] for _ in range(beam_width)]
    best_solution = None
    best_unsat = float('inf')

    for _ in range(max_steps):
        candidate_pool = []
        for solution in beam:
            current_unsat = count_unsatisfied_clauses(clauses, solution)
            if current_unsat < best_unsat:
                best_unsat = current_unsat
                best_solution = solution
            if current_unsat == 0:
                return solution, True

            for var_idx in range(num_vars):
                new_solution = solution[:]
                new_solution[var_idx] = not new_solution[var_idx]
                new_unsat = count_unsatisfied_clauses(clauses, new_solution)
                candidate_pool.append((new_solution, new_unsat))

        # Keep top 'beam_width' candidates with least unsatisfied clauses
        candidate_pool.sort(key=lambda x: x[1])
        beam = [sol for sol, _ in candidate_pool[:beam_width]]

    return best_solution, False


# ------------------------------------------------------------
# Variable Neighborhood Descent (VND)
# ------------------------------------------------------------
def vnd_unsat(clauses, num_vars, max_steps=1000):
    """Uses Variable Neighborhood Descent to reduce unsatisfied clauses."""

    def neighborhood_1(_):
        for i in range(num_vars):
            yield (i,)

    def neighborhood_2(_):
        for i in range(num_vars):
            for j in range(i + 1, num_vars):
                yield (i, j)

    def neighborhood_3(_):
        for i in range(num_vars):
            for j in range(i + 1, num_vars):
                for k in range(j + 1, num_vars):
                    yield (i, j, k)

    neighborhoods = [neighborhood_1, neighborhood_2, neighborhood_3]
    solution = [random.choice([True, False]) for _ in range(num_vars)]

    for _ in range(max_steps):
        current_unsat = count_unsatisfied_clauses(clauses, solution)
        if current_unsat == 0:
            return solution, True

        improved = False
        for neighborhood in neighborhoods:
            for flip_indices in neighborhood(solution):
                new_solution = solution[:]
                for idx in flip_indices:
                    new_solution[idx] = not new_solution[idx]
                new_unsat = count_unsatisfied_clauses(clauses, new_solution)
                if new_unsat < current_unsat:
                    solution = new_solution
                    current_unsat = new_unsat
                    improved = True
                    break
            if improved:
                break

        if not improved:
            break

    return solution, False


# ------------------------------------------------------------
# Experiment Runner
# ------------------------------------------------------------
def run_experiment(num_vars, num_clauses, trials=10):
    """Compares hill climbing, beam search, and VND on random 3-SAT problems."""
    stats = {
        'hill_climb': {'success': 0, 'avg_unsat': 0},
        'beam_3': {'success': 0, 'avg_unsat': 0},
        'beam_4': {'success': 0, 'avg_unsat': 0},
        'vnd': {'success': 0, 'avg_unsat': 0},
    }

    for _ in range(trials):
        clauses = generate_3sat_instance(num_vars, num_clauses)

        # Hill Climbing
        sol, solved = hill_climb_unsat(clauses, num_vars)
        stats['hill_climb']['success'] += int(solved)
        stats['hill_climb']['avg_unsat'] += count_unsatisfied_clauses(clauses, sol)

        # Beam Search (width = 3)
        sol, solved = beam_search_unsat(clauses, num_vars, beam_width=3)
        stats['beam_3']['success'] += int(solved)
        stats['beam_3']['avg_unsat'] += count_unsatisfied_clauses(clauses, sol)

        # Beam Search (width = 4)
        sol, solved = beam_search_unsat(clauses, num_vars, beam_width=4)
        stats['beam_4']['success'] += int(solved)
        stats['beam_4']['avg_unsat'] += count_unsatisfied_clauses(clauses, sol)

        # Variable Neighborhood Descent
        sol, solved = vnd_unsat(clauses, num_vars)
        stats['vnd']['success'] += int(solved)
        stats['vnd']['avg_unsat'] += count_unsatisfied_clauses(clauses, sol)

    for algo in stats:
        stats[algo]['avg_unsat'] /= trials

    return stats


# ------------------------------------------------------------
# Run and Display Results
# ------------------------------------------------------------
num_vars = 20
num_clauses = 80
num_trials = 5

results = run_experiment(num_vars, num_clauses, num_trials)

print(f"n = {num_vars}, m = {num_clauses}")
print("Comparison Results for 3-SAT Problem (Unsatisfied Clause Heuristic):\n")
print(f"Hill Climbing: Success Rate: {results['hill_climb']['success']}/{num_trials}, Avg Unsatisfied: {results['hill_climb']['avg_unsat']:.2f}")
print(f"Beam Search (width=3): Success Rate: {results['beam_3']['success']}/{num_trials}, Avg Unsatisfied: {results['beam_3']['avg_unsat']:.2f}")
print(f"Beam Search (width=4): Success Rate: {results['beam_4']['success']}/{num_trials}, Avg Unsatisfied: {results['beam_4']['avg_unsat']:.2f}")
print(f"VND: Success Rate: {results['vnd']['success']}/{num_trials}, Avg Unsatisfied: {results['vnd']['avg_unsat']:.2f}")

