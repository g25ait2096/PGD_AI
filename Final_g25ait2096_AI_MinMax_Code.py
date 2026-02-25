#Adversarial Search Extension (Minimax Formulation)
import time
from copy import deepcopy

# Goal State
GOAL = ('1','2','3','4','5','6','7','8','B')

# Convert string input to tuple
def parse_input(s):
    s = s.replace(';','').replace(':','')
    return tuple(s)

# Manhattan Distance Heuristic
def manhattan(state):
    distance = 0
    for i, tile in enumerate(state):
        if tile == 'B':
            continue
        goal_index = GOAL.index(tile)
        x1, y1 = divmod(i,3)
        x2, y2 = divmod(goal_index,3)
        distance += abs(x1-x2) + abs(y1-y2)
    return distance

# Generate possible moves
def get_neighbors(state):
    neighbors = []
    idx = state.index('B')
    x,y = divmod(idx,3)
    
    moves = {
        "UP": (-1,0),
        "DOWN": (1,0),
        "LEFT": (0,-1),
        "RIGHT": (0,1)
    }
    
    for move,(dx,dy) in moves.items():
        nx,ny = x+dx,y+dy
        if 0<=nx<3 and 0<=ny<3:
            new_idx = nx*3+ny
            new_state = list(state)
            new_state[idx],new_state[new_idx] = new_state[new_idx],new_state[idx]
            neighbors.append((tuple(new_state),move))
    return neighbors

# Global counter
states_explored = 0

# Minimax
def minimax(state, depth, maximizing):
    global states_explored
    states_explored += 1
    
    if state == GOAL:
        return 100, []
    
    if depth == 0:
        return -manhattan(state), []
    
    neighbors = get_neighbors(state)
    
    if maximizing:
        max_eval = float('-inf')
        best_path = []
        for child,move in neighbors:
            eval_score, path = minimax(child, depth-1, False)
            if eval_score > max_eval:
                max_eval = eval_score
                best_path = [move] + path
        return max_eval, best_path
    else:
        min_eval = float('inf')
        best_path = []
        for child,move in neighbors:
            eval_score, path = minimax(child, depth-1, True)
            if eval_score < min_eval:
                min_eval = eval_score
                best_path = [move] + path
        return min_eval, best_path


# ===========================
# RUN
# ===========================

start_state = parse_input("123;B46:758")

start_time = time.time()

score, path = minimax(start_state, depth=6, maximizing=True)

end_time = time.time()

print("------ OUTPUT ------")
if start_state == GOAL:
    print("Success: Already in goal state")
elif path:
    print("Success: Goal direction found (depth-limited)")
else:
    print("Failure: No solution within depth")

print("Heuristic Used: Manhattan Distance")
print("Depth Limit Used: 6")
print("Sub-Optimal Path:", path)
print("Minimum Moves Found:", len(path))
print("Path Cost:", len(path))
print("Total States Explored:", states_explored)
print("Total Time Taken:", round(end_time-start_time,4),"seconds")