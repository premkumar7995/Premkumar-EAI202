from collections import deque, defaultdict

class Graph:
    def _init_(self, n):
        self.n = n
        self.adj = defaultdict(list)

    def add_edge(self, u, v):
        # undirected graph
        self.adj[u].append(v)
        self.adj[v].append(u)

    # Breadth-First Search
    def bfs(self, start):
        visited = [False] * self.n
        queue = deque([start])
        visited[start] = True
        order = []

        while queue:
            node = queue.popleft()
            order.append(node)

            for nei in self.adj[node]:
                if not visited[nei]:
                    visited[nei] = True
                    queue.append(nei)

        return order

    # Depth-First Search
    def dfs(self, start):
        visited = [False] * self.n
        order = []

        def dfs_util(node):
            visited[node] = True
            order.append(node)
            for nei in self.adj[node]:
                if not visited[nei]:
                    dfs_util(nei)

        dfs_util(start)
        return order

