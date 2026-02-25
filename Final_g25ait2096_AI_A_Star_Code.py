# A* Search Algorithm Implementation in Python
import heapq
import time

START = "123B46758"
GOAL  = "12345678B"

MOVES = {
    0:[1,3], 1:[0,2,4], 2:[1,5],
    3:[0,4,6], 4:[1,3,5,7], 5:[2,4,8],
    6:[3,7], 7:[4,6,8], 8:[5,7]
}

# ---------- Heuristics ----------

def h1(state):
    return sum(1 for i in range(9) if state[i] != GOAL[i] and state[i] != 'B')

goal_pos = {v:i for i,v in enumerate(GOAL)}

def h2(state):
    dist = 0
    for i,v in enumerate(state):
        if v != 'B':
            gi = goal_pos[v]
            dist += abs(i//3 - gi//3) + abs(i%3 - gi%3)
    return dist

# ---------- A* Search ----------

def astar(start, heuristic):
    t0 = time.time()

    open_heap = []
    heapq.heappush(open_heap, (heuristic(start), 0, start, []))
    visited = set()
    explored = 0

    while open_heap:
        f, g, state, path = heapq.heappop(open_heap)

        if state in visited:
            continue
        visited.add(state)
        explored += 1

        if state == GOAL:
            return {
                "success": True,
                "path": path + [state],
                "moves": g,
                "cost": g,
                "explored": explored,
                "time": time.time() - t0
            }

        blank = state.index('B')

        for nxt in MOVES[blank]:
            new_state = list(state)
            new_state[blank], new_state[nxt] = new_state[nxt], new_state[blank]
            new_state = ''.join(new_state)

            if new_state not in visited:
                heapq.heappush(open_heap,
                    (g+1 + heuristic(new_state),
                     g+1,
                     new_state,
                     path + [state])
                )

    return {"success": False}


# ---------- Run Solver ----------

for name, h in [("Misplaced Tiles (h1)", h1), ("Manhattan Distance (h2)", h2)]:
    print("\n==============================")
    print("Heuristic:", name)

    result = astar(START, h)

    if result["success"]:
        print("Success: YES")
        print("Minimum Moves:", result["moves"])
        print("Path Cost:", result["cost"])
        print("States Explored:", result["explored"])
        print("Time Taken:", round(result["time"],6),"sec")
        print("Path:")

        for step in result["path"]:
            print(step[0:3])
            print(step[3:6])
            print(step[6:9])
            print("---")
    else:
        print("Success: NO")