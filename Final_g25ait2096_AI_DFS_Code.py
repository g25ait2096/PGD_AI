# Depth-First Search (DFS): Explore deep into the library's "stacks".
from collections import deque
import time
start_str = "123;B46:758"

# Parse input
rows = start_str.replace(";",":").split(":")
start = tuple("".join(rows))
goal = tuple("12345678B")

dirs = {"Up":-3,"Down":3,"Left":-1,"Right":1}

def valid_moves(state):
    i = state.index("B")
    r,c = divmod(i,3)
    moves=[]
    if r>0: moves.append("Up")
    if r<2: moves.append("Down")
    if c>0: moves.append("Left")
    if c<2: moves.append("Right")
    return moves

def apply(state, move):
    i = state.index("B")
    j = i + dirs[move]
    s = list(state)
    s[i],s[j] = s[j],s[i]
    return tuple(s)

def dfs(start,goal):
    stack=[(start,[])]
    visited=set()
    explored=0
    t0=time.time()

    while stack:
        state,path = stack.pop()
        if state in visited:
            continue
        visited.add(state)
        explored+=1

        if state==goal:
            return True,path,explored,time.time()-t0

        for m in reversed(valid_moves(state)):
            nxt = apply(state,m)
            if nxt not in visited:
                stack.append((nxt,path+[m]))

    return False,[],explored,time.time()-t0


success,path,explored,t = dfs(start,goal)

print("Success:",success)
print("Moves:",len(path))
print("Path:",path)
print("States explored:",explored)
print("Time:",t)