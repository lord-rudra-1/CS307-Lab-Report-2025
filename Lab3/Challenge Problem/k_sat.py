import random

# -----------------------------------------------------------
# 3-SAT Random Instance Generator
# -----------------------------------------------------------
def generate_3sat_instance(num_vars, num_clauses):
    """Generate a random 3-SAT instance with given variables and clauses."""
    problem = []
    for _ in range(num_clauses):
        # Pick 3 unique variables
        vars_in_clause = random.sample(range(1, num_vars + 1), 3)
        # Randomly negate variables
        clause = [v if random.choice([True, False]) else -v for v in vars_in_clause]
        problem.append(clause)
    return problem


# -----------------------------------------------------------
# Clause Weighting Heuristic Function
# -----------------------------------------------------------
def weighted_unsatisfied_sum(clauses, assignment, weights):
    """Compute total weight of unsatisfied clauses under a given assignment."""
    total_weight = 0
    for idx, clause in enumerate(clauses):
        satisfied = any(
            (lit > 0 and assignment[lit - 1]) or (lit < 0 and not assignment[-lit - 1])
            for lit in clause
        )
        if not satisfied:
            total_weight += weights[idx]
    return total_weight


# -----------------------------------------------------------
# Clause Weight Update Rule
# -----------------------------------------------------------
def increment_unsatisfied_weights(clauses, assignment, weights):
    """Increment weights of unsatisfied clauses."""
    for idx, clause in enumerate(clauses):
        satisfied = any(
            (lit > 0 and assignment[lit - 1]) or (lit < 0 and not assignment[-lit - 1])
            for lit in clause
        )
        if not satisfied:
            weights[idx] += 1


# -----------------------------------------------------------
# Hill Climbing with Clause Weighting
# -----------------------------------------------------------
def hill_climb_with_weights(clauses, num_vars, max_steps=1000, restarts=10):
    best_solution = None
    best_score = float('inf')
    weights = [1] * len(clauses)

    for _ in range(restarts):
        assignment = [random.choice([True, False]) for _ in range(num_vars)]
        for _ in range(max_steps):
            score = weighted_unsatisfied_sum(clauses, assignment, weights)
            if score == 0:
                return assignment, True  # Found a solution

            best_flip = None
            best_new_score = score

            for var_idx in range(num_vars):
                assignment[var_idx] = not assignment[var_idx]
                new_score = weighted_unsatisfied_sum(clauses, assignment, weights)
                if new_score < best_new_score:
                    best_new_score = new_score
                    best_flip = var_idx
                assignment[var_idx] = not assignment[var_idx]  # revert

            if best_flip is None:
                break  # Local minimum reached

            assignment[best_flip] = not assignment[best_flip]
            increment_unsatisfied_weights(clauses, assignment, weights)

        if score < best_score:
            best_score = score
            best_solution = assignment

    return best_solution, best_score == 0


# -----------------------------------------------------------
# Beam Search with Clause Weighting
# -----------------------------------------------------------
def beam_search_with_weights(clauses, num_vars, beam_width=5, max_steps=1000):
    beam = [[random.choice([True, False]) for _ in range(num_vars)] for _ in range(beam_width)]
    best_solution = None
    best_score = float('inf')
    weights = [1] * len(clauses)

    for _ in range(max_steps):
        candidates = []
        for assignment in beam:
            score = weighted_unsatisfied_sum(clauses, assignment, weights)
            if score < best_score:
                best_score = score
                best_solution = assignment
            if score == 0:
                return assignment, True

            # Generate neighbors
            for var_idx in range(num_vars):
                new_assignment = assignment[:]
                new_assignment[var_idx] = not new_assignment[var_idx]
                new_score = weighted_unsatisfied_sum(clauses, new_assignment, weights)
                candidates.append((new_assignment, new_score))

        # Keep the top beam_width best candidates
        candidates.sort(key=lambda x: x[1])
        beam = [a for a, _ in candidates[:beam_width]]
        increment_unsatisfied_weights(clauses, beam[0], weights)

    return best_solution, best_score == 0


# -----------------------------------------------------------
# Variable Neighborhood Descent (VND) with Clause Weighting
# -----------------------------------------------------------
def vnd_with_weights(clauses, num_vars, max_steps=1000):
    def neighborhood_flip_1(_):
        for i in range(num_vars):
            yield (i,)

    def neighborhood_flip_2(_):
        for i in range(num_vars):
            for j in range(i + 1, num_vars):
                yield (i, j)

    def neighborhood_flip_3(_):
        for i in range(num_vars):
            for j in range(i + 1, num_vars):
                for k in range(j + 1, num_vars):
                    yield (i, j, k)

    neighborhoods = [neighborhood_flip_1, neighborhood_flip_2, neighborhood_flip_3]
    assignment = [random.choice([True, False]) for _ in range(num_vars)]
    weights = [1] * len(clauses)

    for _ in range(max_steps):
        current_score = weighted_unsatisfied_sum(clauses, assignment, weights)
        if current_score == 0:
            return assignment, True

        improved = False
        for neighborhood in neighborhoods:
            for flip_set in neighborhood(assignment):
                new_assignment = assignment[:]
                for var_idx in flip_set:
                    new_assignment[var_idx] = not new_assignment[var_idx]
                new_score = weighted_unsatisfied_sum(clauses, new_assignment, weights)
                if new_score < current_score:
                    assignment = new_assignment
                    current_score = new_score
                    improved = True
                    break
            if improved:
                break

        if not improved:
            break
        increment_unsatisfied_weights(clauses, assignment, weights)

    return assignment, current_score == 0


# -----------------------------------------------------------
# Experiment Runner
# -----------------------------------------------------------
def run_experiment(num_vars, num_clauses, trials=5):
    """Run and compare all clause-weighting-based algorithms."""
    stats = {
        'hill_climb': {'success': 0, 'avg_unsat_weight': 0},
        'beam_3': {'success': 0, 'avg_unsat_weight': 0},
        'beam_4': {'success': 0, 'avg_unsat_weight': 0},
        'vnd': {'success': 0, 'avg_unsat_weight': 0},
    }

    for _ in range(trials):
        clauses = generate_3sat_instance(num_vars, num_clauses)
        weights = [1] * num_clauses

        # Hill Climbing
        sol, solved = hill_climb_with_weights(clauses, num_vars)
        stats['hill_climb']['success'] += int(solved)
        stats['hill_climb']['avg_unsat_weight'] += weighted_unsatisfied_sum(clauses, sol, weights)

        # Beam Search (width = 3)
        sol, solved = beam_search_with_weights(clauses, num_vars, beam_width=3)
        stats['beam_3']['success'] += int(solved)
        stats['beam_3']['avg_unsat_weight'] += weighted_unsatisfied_sum(clauses, sol, weights)

        # Beam Search (width = 4)
        sol, solved = beam_search_with_weights(clauses, num_vars, beam_width=4)
        stats['beam_4']['success'] += int(solved)
        stats['beam_4']['avg_unsat_weight'] += weighted_unsatisfied_sum(clauses, sol, weights)

        # VND
        sol, solved = vnd_with_weights(clauses, num_vars)
        stats['vnd']['success'] += int(solved)
        stats['vnd']['avg_unsat_weight'] += weighted_unsatisfied_sum(clauses, sol, weights)

    # Compute averages
    for algo in stats:
        stats[algo]['avg_unsat_weight'] /= trials

    return stats


# -----------------------------------------------------------
# Run and Display Results
# -----------------------------------------------------------
num_vars = 20
num_clauses = 80
num_trials = 5

results = run_experiment(num_vars, num_clauses, num_trials)

print(f"\nn = {num_vars}, m = {num_clauses}")
print("3-SAT Clause Weighting Heuristic: Algorithm Comparison\n")
print(f"Hill Climbing: Success {results['hill_climb']['success']}/{num_trials}, Avg Unsatisfied Weight: {results['hill_climb']['avg_unsat_weight']:.2f}")
print(f"Beam Search (width=3): Success {results['beam_3']['success']}/{num_trials}, Avg Unsatisfied Weight: {results['beam_3']['avg_unsat_weight']:.2f}")
print(f"Beam Search (width=4): Success {results['beam_4']['success']}/{num_trials}, Avg Unsatisfied Weight: {results['beam_4']['avg_unsat_weight']:.2f}")
print(f"VND: Success {results['vnd']['success']}/{num_trials}, Avg Unsatisfied Weight: {results['vnd']['avg_unsat_weight']:.2f}")
