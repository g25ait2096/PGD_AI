#Greedy Best-First Search: Prioritize based on immediate appearance.
import heapq
import time

start = "123B46758"
goal = "12345678B"

# Goal positions
goal_pos = {goal[i]: (i//3, i%3) for i in range(9)}

# Manhattan heuristic
def heuristic(state):
    dist = 0
    for i, tile in enumerate(state):
        if tile == 'B':
            continue
        x, y = i//3, i%3
        gx, gy = goal_pos[tile]
        dist += abs(x-gx) + abs(y-gy)
    return dist

# Generate neighbors
def neighbors(state):
    idx = state.index('B')
    x, y = idx//3, idx%3
    moves = []

    directions = {
        "Up": (x-1, y),
        "Down": (x+1, y),
        "Left": (x, y-1),
        "Right": (x, y+1)
    }

    for move, (nx, ny) in directions.items():
        if 0 <= nx < 3 and 0 <= ny < 3:
            nidx = nx*3 + ny
            new_state = list(state)
            new_state[idx], new_state[nidx] = new_state[nidx], new_state[idx]
            moves.append(("".join(new_state), move))
    return moves

def greedy_bfs(start):
    start_time = time.time()

    pq = []
    heapq.heappush(pq, (heuristic(start), start, []))
    visited = set()

    states_explored = 0

    while pq:
        h, state, path = heapq.heappop(pq)

        if state in visited:
            continue
        visited.add(state)
        states_explored += 1

        if state == goal:
            end_time = time.time()
            return {
                "success": True,
                "path": path,
                "moves": len(path),
                "states": states_explored,
                "cost": len(path),
                "time": end_time - start_time
            }

        for nxt, move in neighbors(state):
            if nxt not in visited:
                heapq.heappush(pq, (heuristic(nxt), nxt, path + [move]))

    return {"success": False}


# Run
result = greedy_bfs(start)

# Output Greedy Best-First Search results
if result["success"]:
    print("SUCCESS\n")
    print("Heuristic Used: Manhattan Distance")
    print("Moves:", result["moves"])
    print("Path:", result["path"])
    print("Total States Explored:", result["states"])
    print("Path Cost:", result["cost"])
    print("Time Taken:", result["time"], "seconds")
else:
    print("FAILURE: No solution found")