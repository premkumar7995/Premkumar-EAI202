from collections import deque
import heapq


graph = {}

def add_edge(u, v, cost):
    if u not in graph:
        graph[u] = []
    if v not in graph:
        graph[v] = []
    graph[u].append((v, cost))
    graph[v].append((u, cost))  


def dfs(start, target):
    stack = [(start, [start], 0)]
    visited = set()
    
    while stack:
        node, path, cost = stack.pop()
        if node == target:
            return path, cost
        
        if node not in visited:
            visited.add(node)
            for neighbor, c in graph.get(node, []):
                if neighbor not in visited:
                    stack.append((neighbor, path + [neighbor], cost + c))
    return None, float("inf")


def bfs(start, target):
    queue = deque([(start, [start], 0)])
    visited = set([start])
    
    while queue:
        node, path, cost = queue.popleft()
        if node == target:
            return path, cost
        for neighbor, c in graph.get(node, []):
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, path + [neighbor], cost + c))
    return None, float("inf")

def dijkstra(start, target):
    pq = [(0, start, [start])] 
    visited = set()
    
    while pq:
        cost, node, path = heapq.heappop(pq)
        if node == target:
            return path, cost
        if node in visited:
            continue
        visited.add(node)
        for neighbor, c in graph.get(node, []):
            if neighbor not in visited:
                heapq.heappush(pq, (cost + c, neighbor, path + [neighbor]))
    return None, float("inf")


if __name__ == "__main__":
   
    add_edge(1, 2, 4)
    add_edge(1, 3, 2)
    add_edge(2, 4, 5)
    add_edge(3, 4, 1)
    add_edge(4, 5, 3)

    start, target = 1, 5

    dfs_path, dfs_cost = dfs(start, target)
    bfs_path, bfs_cost = bfs(start, target)
    dijkstra_path, dijkstra_cost = dijkstra(start, target)

    print("DFS Path:", dfs_path, "Cost:", dfs_cost)
    print("BFS Path:", bfs_path, "Cost:", bfs_cost)
    print("Dijkstra (Lowest Cost) Path:", dijkstra_path, "Cost:", dijkstra_cost)
