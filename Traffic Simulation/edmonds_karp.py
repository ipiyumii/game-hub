from collections import defaultdict, deque
from timer import timer

class EdmondsKarpBFS:
    def __init__(self):
        pass

    @timer
    def max_flow(self, graph, source, sink):
        """Edmonds-Karp algorithm using BFS"""
        # Create residual graph
        residual_graph = defaultdict(dict)
        for u in graph:
            for v, cap in graph[u].items():
                residual_graph[u][v] = cap
                residual_graph[v].setdefault(u, 0)

        max_flow = 0
        parent = {}

        while self.bfs(residual_graph, source, sink, parent):
            # Find minimum residual capacity along the path
            path_flow = float('inf')
            s = sink

            while s != source:
                path_flow = min(path_flow, residual_graph[parent[s]][s])
                s = parent[s]

            # Update residual capacities and reverse edges
            v = sink
            while v != source:
                u = parent[v]
                residual_graph[u][v] -= path_flow
                residual_graph[v][u] += path_flow
                v = parent[v]

            max_flow += path_flow
            parent.clear()

        return max_flow

    def bfs(self, graph, source, sink, parent):
        """Breadth-First Search to find augmenting path"""
        visited = set()
        queue = deque([source])
        visited.add(source)

        while queue:
            u = queue.popleft()

            for v, capacity in graph[u].items():
                if v not in visited and capacity > 0:
                    visited.add(v)
                    parent[v] = u

                    if v == sink:
                        return True

                    queue.append(v)

        return False


# Factory function to create Edmonds-Karp instance
def create_edmonds_karp():
    return EdmondsKarpBFS()