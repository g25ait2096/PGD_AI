import time
from collections import deque
import networkx as nx
import matplotlib.pyplot as plt

# 1. PROBLEM DEFINITION

slots = ["Slot1", "Slot2", "Slot3", "Slot4"]
bots = ["A", "B", "C"]

domains = {
    "Slot1": set(bots),
    "Slot2": set(bots),
    "Slot3": set(bots),
    "Slot4": set(bots) - {"C"}  # Maintenance constraint
}

neighbors = {
    "Slot1": ["Slot2"],
    "Slot2": ["Slot1", "Slot3"],
    "Slot3": ["Slot2", "Slot4"],
    "Slot4": ["Slot3"]
}

assignments_count = 0
step_counter = 0

# 2. CONSTRAINT GRAPH DIAGRAM

def draw_constraint_graph():
    G = nx.Graph()
    G.add_nodes_from(slots)

    for var in neighbors:
        for n in neighbors[var]:
            G.add_edge(var, n)

    plt.figure(figsize=(5,4))
    nx.draw(G, with_labels=True, node_color="lightblue", node_size=2000)
    plt.title("Constraint Graph (No Back-to-Back)")
    plt.show()

# 3. CONSISTENCY CHECK

def is_consistent(var, value, assignment):
    for n in neighbors[var]:
        if n in assignment and assignment[n] == value:
            return False
    return True

# 4. MRV HEURISTIC

def select_unassigned_variable(assignment, domains):
    unassigned = [v for v in slots if v not in assignment]
    return min(unassigned, key=lambda var: len(domains[var]))

# 5. FORWARD CHECKING

def forward_check(var, value, domains, assignment):
    new_domains = {v: domains[v].copy() for v in domains}

    for n in neighbors[var]:
        if n not in assignment and value in new_domains[n]:
            new_domains[n].remove(value)
            if not new_domains[n]:
                return None
    return new_domains

# 6. MINIMUM COVERAGE

def minimum_coverage_satisfied(assignment):
    used = set(assignment.values())
    return all(bot in used for bot in bots)

# 7. BACKTRACKING SEARCH

def backtrack(assignment, domains):
    global assignments_count, step_counter

    if len(assignment) == len(slots):
        if minimum_coverage_satisfied(assignment):
            return assignment
        return None

    var = select_unassigned_variable(assignment, domains)

    for value in sorted(domains[var]):
        if is_consistent(var, value, assignment):

            assignments_count += 1

            if step_counter < 3:
                step_counter += 1
                print(f"\nSTEP {step_counter}")
                print("Selected Variable (MRV):", var)
                print("Trying Value:", value)
                print("Current Assignment:", assignment)

            assignment[var] = value
            new_domains = forward_check(var, value, domains, assignment)

            if new_domains is not None:
                result = backtrack(assignment, new_domains)
                if result:
                    return result

            del assignment[var]

    return None

# 8. AC-3 ALGORITHM

def revise(domains, xi, xj):
    revised = False
    to_remove = set()

    for x in domains[xi]:
        if all(x == y for y in domains[xj]):
            to_remove.add(x)
            revised = True

    domains[xi] -= to_remove
    return revised


def ac3(domains):
    queue = deque([(xi, xj) for xi in slots for xj in neighbors[xi]])

    while queue:
        xi, xj = queue.popleft()
        if revise(domains, xi, xj):
            if not domains[xi]:
                return False
            for xk in neighbors[xi]:
                if xk != xj:
                    queue.append((xk, xi))
    return True

# MAIN EXECUTION

if __name__ == "__main__":

    print("Running AC-3...")
    ac3(domains)

    print("\nSolving CSP...\n")
    start = time.time()
    solution = backtrack({}, domains)
    end = time.time()

    if solution:
        print("\nSolution Found:")
        for k in sorted(solution):
            print(k, "→", solution[k])
    else:
        print("No solution found.")

    print("\nAssignments tried:", assignments_count)
    print("Time taken:", round(end-start,4), "seconds")

    draw_constraint_graph()