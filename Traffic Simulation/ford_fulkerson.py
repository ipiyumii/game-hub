from collections import defaultdict
from timer import timer

class FordFulkersonDFS:
    def __init__(self):
        self.visited = set()

    @timer
    def max_flow(self, graph, source, sink):
        # Create residual graph
        residual_graph = defaultdict(dict)
        for u in graph:
            for v, cap in graph[u].items():
                residual_graph[u][v] = cap
                residual_graph[v].setdefault(u, 0)

        max_flow = 0

        while True:
            self.visited.clear()
            path_flow = self.dfs(residual_graph, source, sink, float('inf'))

            if path_flow == 0:
                break

            max_flow += path_flow

        return max_flow

    def dfs(self, graph, u, sink, flow):
        if u == sink:
            return flow

        self.visited.add(u)

        for v, capacity in graph[u].items():
            if v not in self.visited and capacity > 0:
                min_capacity = min(flow, capacity)
                path_flow = self.dfs(graph, v, sink, min_capacity)

                if path_flow > 0:
                    graph[u][v] -= path_flow
                    graph[v][u] += path_flow
                    return path_flow

        return 0

# create Ford-Fulkerson instance
def create_ford_fulkerson():
    return FordFulkersonDFS()