#MinMax with Alpha–Beta Pruning
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
ab_states_explored = 0


# -------------------------
# Minimax
# -------------------------
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


# -------------------------
# Alpha-Beta Minimax
# -------------------------
def alphabeta(state, depth, alpha, beta, maximizing):
    global ab_states_explored
    ab_states_explored += 1
    
    if state == GOAL:
        return 100, []
    
    if depth == 0:
        return -manhattan(state), []
    
    neighbors = get_neighbors(state)
    
    if maximizing:
        max_eval = float('-inf')
        best_path = []
        for child,move in neighbors:
            eval_score, path = alphabeta(child, depth-1, alpha, beta, False)
            
            if eval_score > max_eval:
                max_eval = eval_score
                best_path = [move] + path
            
            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break   # PRUNING
        
        return max_eval, best_path
    
    else:
        min_eval = float('inf')
        best_path = []
        for child,move in neighbors:
            eval_score, path = alphabeta(child, depth-1, alpha, beta, True)
            
            if eval_score < min_eval:
                min_eval = eval_score
                best_path = [move] + path
            
            beta = min(beta, min_eval)
            if beta <= alpha:
                break   # PRUNING
        
        return min_eval, best_path


# ===========================
# RUN
# ===========================

start_state = parse_input("123;B46:758")

# ---- Minimax ----
start_time = time.time()
score, path = minimax(start_state, depth=6, maximizing=True)
end_time = time.time()

minimax_time = end_time - start_time

# ---- Alpha Beta ----
ab_start = time.time()
ab_score, ab_path = alphabeta(start_state, 6, float('-inf'), float('inf'), True)
ab_end = time.time()

ab_time = ab_end - ab_start


print("------ MINIMAX OUTPUT ------")
if start_state == GOAL:
    print("Success: Already in goal state")
elif path:
    print("Success: Goal direction found (depth-limited)")
else:
    print("Failure: No solution within depth")

print("Heuristic Used: Manhattan Distance")
print("Depth Limit Used: 6")
print("Path:", path)
print("Moves:", len(path))
print("States Explored:", states_explored)
print("Time:", round(minimax_time,4),"seconds")


print("\n------ ALPHA-BETA OUTPUT ------")
if ab_path:
    print("Success: Goal direction found (depth-limited)")
else:
    print("Failure: No solution within depth")

print("Path:", ab_path)
print("Moves:", len(ab_path))
print("States Explored:", ab_states_explored)
print("Time:", round(ab_time,4),"seconds")


print("\n------ EFFICIENCY COMPARISON ------")
print("Minimax States:", states_explored)
print("AlphaBeta States:", ab_states_explored)
print("Pruning Improvement:",
      round(states_explored/ab_states_explored,2),"x fewer states explored")