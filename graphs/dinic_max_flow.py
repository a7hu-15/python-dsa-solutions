"""
Dinic's Algorithm for Maximum Network Flow in Python.

Dinic's algorithm is a strongly polynomial algorithm for computing the maximum flow
in a flow network. It uses Breadth-First Search (BFS) to construct a level graph
and Depth-First Search (DFS) with current-edge pointers to push blocking flows.

Complexity Analysis:
- Time Complexity: O(V^2 * E) for general networks.
  - O(E * sqrt(V)) for unit network / bipartite matching.
- Space Complexity: O(V + E) for adjacency list and level graph.
"""

from typing import List, Dict
from collections import deque


class Edge:
    """Represents a directed network flow edge with residual capacity."""

    def __init__(self, to: int, rev_idx: int, capacity: int):
        self.to = to
        self.rev_idx = rev_idx
        self.capacity = capacity
        self.flow = 0


class Dinic:
    """
    Dinic's Maximum Flow Solver.

    >>> dinic = Dinic(4)
    >>> dinic.add_edge(0, 1, 10)
    >>> dinic.add_edge(0, 2, 10)
    >>> dinic.add_edge(1, 2, 2)
    >>> dinic.add_edge(1, 3, 4)
    >>> dinic.add_edge(2, 3, 8)
    >>> dinic.max_flow(0, 3)
    12
    """

    def __init__(self, n: int):
        self.n = n
        self.graph: List[List[Edge]] = [[] for _ in range(n)]
        self.level: List[int] = []
        self.ptr: List[int] = []

    def add_edge(self, u: int, v: int, capacity: int) -> None:
        """Add a directed edge u -> v with given capacity and a residual back-edge."""
        forward = Edge(v, len(self.graph[v]), capacity)
        backward = Edge(u, len(self.graph[u]), 0)
        self.graph[u].append(forward)
        self.graph[v].append(backward)

    def _bfs(self, source: int, sink: int) -> bool:
        """Build level graph using BFS."""
        self.level = [-1] * self.n
        self.level[source] = 0
        queue = deque([source])

        while queue:
            node = queue.popleft()
            for edge in self.graph[node]:
                if edge.capacity - edge.flow > 0 and self.level[edge.to] == -1:
                    self.level[edge.to] = self.level[node] + 1
                    queue.append(edge.to)

        return self.level[sink] != -1

    def _dfs(self, node: int, sink: int, pushed: int) -> int:
        """Push blocking flow using DFS along the level graph."""
        if pushed == 0 or node == sink:
            return pushed

        for i in range(self.ptr[node], len(self.graph[node])):
            self.ptr[node] = i
            edge = self.graph[node][i]
            tr = edge.to

            if self.level[node] + 1 != self.level[tr] or edge.capacity - edge.flow == 0:
                continue

            push = self._dfs(tr, sink, min(pushed, edge.capacity - edge.flow))
            if push == 0:
                continue

            edge.flow += push
            self.graph[tr][edge.rev_idx].flow -= push
            return push

        return 0

    def max_flow(self, source: int, sink: int) -> int:
        """
        Compute maximum flow from source to sink in O(V^2 E).
        """
        if source == sink:
            return 0

        flow = 0
        INF = 10**18

        while self._bfs(source, sink):
            self.ptr = [0] * self.n
            while True:
                pushed = self._dfs(source, sink, INF)
                if pushed == 0:
                    break
                flow += pushed

        return flow


if __name__ == "__main__":
    import doctest

    results = doctest.testmod()
    if results.failed == 0:
        print(f"All {results.attempted} Dinic doctests passed successfully!")
