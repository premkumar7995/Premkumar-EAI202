import heapq
import math



grid = [
    ["S", "0", "0", "1", "0"],
    ["1", "1", "0", "1", "G"],
    ["0", "0", "0", "1", "0"],
    ["1", "1", "0", "1", "1"],
    ["0", "0", "0", "0", "0"]
]

ROWS, COLS = len(grid), len(grid[0])




def find_position(symbol):
    for r in range(ROWS):
        for c in range(COLS):
            if grid[r][c] == symbol:
                return (r, c)
    return None

start = find_position("S")
goal = find_position("G")

def in_bounds(r, c):
    return 0 <= r < ROWS and 0 <= c < COLS

def passable(r, c):
    return grid[r][c] != "1"

def neighbors(pos, allow_diagonal=False):
    (r, c) = pos
    steps = [(1,0), (-1,0), (0,1), (0,-1)]
    if allow_diagonal:
        steps += [(1,1), (1,-1), (-1,1), (-1,-1)]
    for dr, dc in steps:
        nr, nc = r + dr, c + dc
        if in_bounds(nr, nc) and passable(nr, nc):
            yield (nr, nc)



def manhattan(a, b):
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def euclidean(a, b):
    return math.sqrt((a[0]-b[0])**2 + (a[1]-b[1])**2)

def diagonal(a, b):
    return max(abs(a[0]-b[0]), abs(a[1]-b[1]))




def reconstruct_path(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path




def greedy_best_first(start, goal, heuristic):
    frontier = []
    heapq.heappush(frontier, (heuristic(start, goal), start))
    came_from = {start: None}

    while frontier:
        _, current = heapq.heappop(frontier)

        if current == goal:
            break

        for nxt in neighbors(current):
            if nxt not in came_from:
                heapq.heappush(frontier, (heuristic(nxt, goal), nxt))
                came_from[nxt] = current

    return reconstruct_path(came_from, start, goal)




path = greedy_best_first(start, goal, manhattan)
print("Path found:", path)
