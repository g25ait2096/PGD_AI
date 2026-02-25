#Simulated Annealing_Define a cooling schedule and use the same to evaluate the probability P=e^(-△E/T) to escape local maxima by occasionally accepting "worse" moves.
import random
import math
import time

# -----------------------------
# Problem Definition
# -----------------------------
START = "123B46758"
GOAL = "12345678B"

# goal positions for Manhattan distance
goal_pos = {c:(i//3, i%3) for i,c in enumerate(GOAL)}

# -----------------------------
# Heuristic (Energy Function)
# -----------------------------
def energy(state):
    dist = 0
    for i,c in enumerate(state):
        if c != 'B':
            r,curr = i//3, i%3
            gr,gc = goal_pos[c]
            dist += abs(r-gr)+abs(curr-gc)
    return dist

# -----------------------------
# Generate neighbors
# -----------------------------
def neighbors(state):
    idx = state.index('B')
    r,c = idx//3, idx%3
    moves = []
    directions = [(-1,0),(1,0),(0,-1),(0,1)]

    for dr,dc in directions:
        nr,nc = r+dr, c+dc
        if 0<=nr<3 and 0<=nc<3:
            nidx = nr*3+nc
            s = list(state)
            s[idx], s[nidx] = s[nidx], s[idx]
            moves.append("".join(s))
    return moves

# -----------------------------
# Simulated Annealing Solver
# -----------------------------
def simulated_annealing(start,
                        T=1000,
                        cooling_rate=0.995,
                        Tmin=0.001,
                        max_steps=100000):

    current = start
    current_E = energy(current)
    path = [current]
    explored = 0

    start_time = time.time()

    while T > Tmin and explored < max_steps:
        if current == GOAL:
            break

        next_state = random.choice(neighbors(current))
        next_E = energy(next_state)

        dE = next_E - current_E

        # accept better state
        if dE < 0:
            accept = True
        else:
            prob = math.exp(-dE/T)
            accept = random.random() < prob

        if accept:
            current = next_state
            current_E = next_E
            path.append(current)

        T *= cooling_rate
        explored += 1

    end_time = time.time()

    success = current == GOAL

    return {
        "success": success,
        "path": path,
        "moves": len(path)-1,
        "states_explored": explored,
        "time": end_time-start_time,
        "final_state": current
    }

# -----------------------------
# Run Solver
# -----------------------------
result = simulated_annealing(START)

print("Success:", result["success"])
print("Final State:", result["final_state"])
print("Minimum Moves Found:", result["moves"])
print("Total States Explored:", result["states_explored"])
print("Total Time Taken:", round(result["time"],5),"seconds")
print("Path Cost:", result["moves"])

print("\nPath:")
for step in result["path"]:
    print(step[:3])
    print(step[3:6])
    print(step[6:])
    print("-----")