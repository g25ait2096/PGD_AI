<<<<<<< HEAD
<<<<<<<< HEAD:Final_g25ait2096_AI_BFS_Code.py
=======
>>>>>>> 4878bbc (uploding DFS)
#A system glitch has scrambled a 3x3 shelf of rare manuscripts.
#Program a robotic sorter to restore order using the BFS algorithms to organize the library:
import time
from collections import deque

# Given Data----------
START = (1,2,3,'B',4,6,7,5,8)
GOAL  = (1,2,3,4,5,6,7,8,'B')

# ---------- Neighbor Generator ----------
def neighbors(state):
    i = state.index('B')
    row, col = divmod(i,3)

    moves = {
        "Up": (-1,0),
        "Down": (1,0),
        "Left": (0,-1),
        "Right": (0,1)
    }

    result = []

    for action,(dr,dc) in moves.items():
        r,c = row+dr, col+dc
        if 0<=r<3 and 0<=c<3:
            j = r*3+c
            s = list(state)
            s[i], s[j] = s[j], s[i]
            result.append((tuple(s),action))
    return result

# ---------- BFS Solver ----------
def bfs(start):
    start_time = time.time()

    queue = deque([(start, [], 0)])
    visited = set()
    explored = 0

    while queue:
        state, path, cost = queue.popleft()
        explored += 1

        if state == GOAL:
            return True, path, cost, explored, time.time()-start_time

        visited.add(state)

        for nxt, action in neighbors(state):
            if nxt not in visited:
                queue.append((nxt, path+[action], cost+1))

    return False, [], 0, explored, time.time()-start_time

# ---------- Run ----------
success, path, cost, states, t = bfs(START)

# ---------- Output ----------
print("\n===== BFS RESULT =====")
print("Start State:", START)
print("Goal State:", GOAL)
print("Success:", success)
print("Heuristic Used: None (BFS)")
print("States Explored:", states)
print("Total Time Taken:", round(t,5),"seconds")

if success:
    print("Minimum Moves:", len(path))
    print("Path Cost:", cost)
    print("Optimal Path:", path)
else:
<<<<<<< HEAD
    print("Failure: No solution found.")
========
>>>>>>>> 4878bbc (uploding DFS):Final_g25ait2096_AI_DFS_Code.py
=======
    print("Failure: No solution found.")
>>>>>>> 4878bbc (uploding DFS)
