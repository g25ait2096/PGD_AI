# a.Iterative Deepening A* (IDA*): Use the same heuristics as A* but with depth-bound adjustments
import time

START = "123B46758"      # given start state
GOAL = "12345678B"

MOVES = {
    0:[1,3], 1:[0,2,4], 2:[1,5],
    3:[0,4,6], 4:[1,3,5,7], 5:[2,4,8],
    6:[3,7], 7:[4,6,8], 8:[5,7]
}

# ---------- HEURISTICS ----------

def h1(state):
    return sum(1 for i in range(9) if state[i] != GOAL[i] and state[i] != 'B')

goal_pos = {GOAL[i]:i for i in range(9)}

def h2(state):
    dist = 0
    for i,ch in enumerate(state):
        if ch != 'B':
            gi = goal_pos[ch]
            dist += abs(i//3 - gi//3) + abs(i%3 - gi%3)
    return dist

def heuristic(state, mode):
    return h1(state) if mode==1 else h2(state)

# ---------- IDA* SEARCH ----------

def ida_star(start, mode):
    start_time = time.time()
    bound = heuristic(start, mode)
    path = [start]
    states = 0

    def search(g, bound):
        nonlocal states
        node = path[-1]
        f = g + heuristic(node, mode)

        if f > bound:
            return f

        if node == GOAL:
            return "FOUND"

        min_bound = float('inf')
        states += 1

        blank = node.index('B')

        for nxt in MOVES[blank]:
            new = list(node)
            new[blank], new[nxt] = new[nxt], new[blank]
            new = "".join(new)

            if new not in path:
                path.append(new)
                t = search(g+1, bound)

                if t == "FOUND":
                    return "FOUND"

                if t < min_bound:
                    min_bound = t

                path.pop()

        return min_bound

    while True:
        t = search(0, bound)
        if t == "FOUND":
            return path, states, time.time()-start_time
        if t == float('inf'):
            return None, states, time.time()-start_time
        bound = t

# ---------- RUN BOTH HEURISTICS ----------

for mode in [1,2]:
    print("\n===== Running IDA* with h{} =====".format(mode))
    path, explored, t = ida_star(START, mode)

    if path:
        print("Success")
        print("Moves =", len(path)-1)
        print("States explored =", explored)
        print("Time =", round(t,4),"seconds")
        print("\nPath:")
        for p in path:
            print(p[0:3])
            print(p[3:6])
            print(p[6:9])
            print("---")
    else:
        print("Failure")