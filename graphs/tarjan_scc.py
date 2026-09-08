"""
Tarjan's Strongly Connected Components (SCC) Algorithm for Directed Graphs.

A Strongly Connected Component (SCC) of a directed graph is a maximal subgraph
where every vertex is reachable from every other vertex in the component.

Time Complexity: O(V + E)
Space Complexity: O(V + E)
"""

from typing import Dict, List, Set, Tuple


class TarjanSCC:
    """Computes Strongly Connected Components (SCCs) in a directed graph using Tarjan's linear-time DFS algorithm."""

    def __init__(self, num_vertices: int):
        if num_vertices < 0:
            raise ValueError("Number of vertices cannot be negative")
        self.num_vertices = num_vertices
        self.adj_list: Dict[int, List[int]] = {i: [] for i in range(num_vertices)}

    def add_edge(self, u: int, v: int) -> None:
        """Adds a directed edge from vertex u to vertex v."""
        if not (0 <= u < self.num_vertices and 0 <= v < self.num_vertices):
            raise ValueError(f"Vertex indices out of bounds [0, {self.num_vertices - 1}]")
        self.adj_list[u].append(v)

    def find_sccs(self) -> List[List[int]]:
        """
        Finds all Strongly Connected Components (SCCs).

        Returns:
            List[List[int]]: List of SCCs, where each SCC is a list of vertex indices.
        """
        timer = 0
        discovery_time = [-1] * self.num_vertices
        low = [-1] * self.num_vertices
        on_stack = [False] * self.num_vertices
        stack: List[int] = []
        sccs: List[List[int]] = []

        def dfs(u: int) -> None:
            nonlocal timer
            discovery_time[u] = low[u] = timer
            timer += 1
            stack.append(u)
            on_stack[u] = True

            for v in self.adj_list[u]:
                if discovery_time[v] == -1:
                    dfs(v)
                    low[u] = min(low[u], low[v])
                elif on_stack[v]:
                    low[u] = min(low[u], discovery_time[v])

            # Root node of SCC found
            if low[u] == discovery_time[u]:
                component: List[int] = []
                while True:
                    node = stack.pop()
                    on_stack[node] = False
                    component.append(node)
                    if node == u:
                        break
                sccs.append(sorted(component))

        for i in range(self.num_vertices):
            if discovery_time[i] == -1:
                dfs(i)

        return sccs


def find_strongly_connected_components(num_vertices: int, edges: List[Tuple[int, int]]) -> List[List[int]]:
    """
    Helper function to compute SCCs given vertex count and list of directed edges (u, v).

    >>> find_strongly_connected_components(5, [(0, 2), (2, 1), (1, 0), (0, 3), (3, 4)])
    [[4], [3], [0, 1, 2]]
    """
    g = TarjanSCC(num_vertices)
    for u, v in edges:
        g.add_edge(u, v)
    return g.find_sccs()
