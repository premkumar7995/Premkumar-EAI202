from flask import Flask, render_template, request, jsonify
from collections import deque
import heapq

app = Flask(__name__)

# Campus locations with coordinates
locations = {
    "Main Gate": [13.2200, 77.7539],
    "ID Gate": [13.2214, 77.7549],
    "Flag Pole": [13.2218, 77.7550],
    "Admin Block": [13.2222, 77.7552],
    "Library": [13.221971, 77.75558],
    "Vend": [13.222264, 77.755126],
    "Cafeteria": [13.22242, 77.755158],
    "Lawn Area": [13.222775, 77.755576],
    "Block 2": [13.22336, 77.755963],
    "Food Court": [13.224758, 77.75725],
    "Hostel": [13.224195, 77.758613],
    "Sports Area": [13.22887, 77.7572]
}

# Define paths between locations (edges with approximate distances in meters)
edges = [
    ["Main Gate", "ID Gate", 50],
    ["ID Gate", "Flag Pole", 30],
    ["Flag Pole", "Admin Block", 40],
    ["Admin Block", "Library", 25],
    ["Admin Block", "Vend", 20],
    ["Vend", "Cafeteria", 15],
    ["Library", "Lawn Area", 35],
    ["Lawn Area", "Block 2", 45],
    ["Block 2", "Food Court", 80],
    ["Food Court", "Hostel", 60],
    ["Hostel", "Sports Area", 200],
    ["Cafeteria", "Lawn Area", 30],
    ["Library", "Vend", 25]
]

# Build the graph
graph = {}
for u, v, w in edges:
    if u not in graph:
        graph[u] = []
    if v not in graph:
        graph[v] = []
    graph[u].append((v, w))
    graph[v].append((u, w))  # Undirected graph

# BFS Algorithm
def bfs(start, goal):
    if start not in graph or goal not in graph:
        return None
    
    queue = deque([[start]])
    visited = set()

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == goal:
            return path

        if node not in visited:
            visited.add(node)
            for neighbor, _ in graph.get(node, []):
                if neighbor not in visited:
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
    return None

# DFS Algorithm
def dfs(start, goal):
    if start not in graph or goal not in graph:
        return None
    
    stack = [[start]]
    visited = set()

    while stack:
        path = stack.pop()
        node = path[-1]

        if node == goal:
            return path

        if node not in visited:
            visited.add(node)
            for neighbor, _ in graph.get(node, []):
                if neighbor not in visited:
                    new_path = list(path)
                    new_path.append(neighbor)
                    stack.append(new_path)
    return None

# UCS Algorithm
def ucs(start, goal):
    if start not in graph or goal not in graph:
        return None, float('inf')
    
    pq = [(0, [start])]
    visited = set()

    while pq:
        cost, path = heapq.heappop(pq)
        node = path[-1]

        if node == goal:
            return path, cost

        if node not in visited:
            visited.add(node)
            for neighbor, weight in graph.get(node, []):
                if neighbor not in visited:
                    new_cost = cost + weight
                    new_path = list(path)
                    new_path.append(neighbor)
                    heapq.heappush(pq, (new_cost, new_path))
    return None, float('inf')

@app.route('/')
def index():
    return render_template('index.html', locations=sorted(locations.keys()))

@app.route('/find_path', methods=['POST'])
def find_path():
    data = request.get_json()
    start = data.get('start')
    goal = data.get('goal')
    algorithm = data.get('algorithm')
    
    if not start or not goal or not algorithm:
        return jsonify({'error': 'Missing parameters'}), 400
    
    if start == goal:
        return jsonify({
            'path': [start],
            'cost': 0,
            'success': True
        })
    
    if algorithm == 'bfs':
        path = bfs(start, goal)
        cost = None
    elif algorithm == 'dfs':
        path = dfs(start, goal)
        cost = None
    elif algorithm == 'ucs':
        path, cost = ucs(start, goal)
    else:
        return jsonify({'error': 'Invalid algorithm'}), 400
    
    if path:
        return jsonify({
            'path': path,
            'cost': cost,
            'success': True
        })
    else:
        return jsonify({
            'path': [],
            'cost': None,
            'success': False,
            'error': 'No path found between the selected locations'
        })

if __name__ == '__main__':
    app.run(debug=True)
