"""
Articulation Points and Bridges in Undirected Graphs using Tarjan's DFS Algorithm.

An articulation point (or cut vertex) is a vertex whose removal increases the number of connected components in a graph.
A bridge (or cut edge) is an edge whose removal increases the number of connected components in a graph.

Time Complexity: O(V + E)
Space Complexity: O(V + E)
"""

from typing import List, Tuple, Set, Dict


class GraphCutAnalyzer:
    """Finds all articulation points and bridges in an undirected graph using Tarjan's DFS approach."""

    def __init__(self, num_vertices: int):
        self.num_vertices = num_vertices
        self.adj_list: Dict[int, List[int]] = {i: [] for i in range(num_vertices)}

    def add_edge(self, u: int, v: int) -> None:
        """Adds an undirected edge between vertices u and v."""
        if not (0 <= u < self.num_vertices and 0 <= v < self.num_vertices):
            raise ValueError(f"Vertex indices out of bounds [0, {self.num_vertices - 1}]")
        self.adj_list[u].append(v)
        self.adj_list[v].append(u)

    def find_articulation_points_and_bridges(self) -> Tuple[Set[int], List[Tuple[int, int]]]:
        """
        Executes Tarjan's DFS traversal to detect cut vertices and cut edges.

        Returns:
            Tuple[Set[int], List[Tuple[int, int]]]:
                - Set of articulation points (vertex IDs)
                - List of bridges formatted as sorted (u, v) tuples where u < v
        """
        timer = 0
        visited = [False] * self.num_vertices
        discovery_time = [0] * self.num_vertices
        low = [0] * self.num_vertices
        parent = [-1] * self.num_vertices
        
        articulation_points: Set[int] = set()
        bridges: List[Tuple[int, int]] = []

        def dfs(u: int) -> None:
            nonlocal timer
            visited[u] = True
            discovery_time[u] = low[u] = timer
            timer += 1
            children = 0

            for v in self.adj_list[u]:
                if v == parent[u]:
                    continue

                if visited[v]:
                    # Back edge: update low[u] using discovery_time[v]
                    low[u] = min(low[u], discovery_time[v])
                else:
                    # Forward edge in DFS tree
                    children += 1
                    parent[v] = u
                    dfs(v)

                    # Check if subtree rooted at v has a connection to an ancestor of u
                    low[u] = min(low[u], low[v])

                    # Condition 1 for Articulation Point: Non-root vertex u and low[v] >= discovery_time[u]
                    if parent[u] != -1 and low[v] >= discovery_time[u]:
                        articulation_points.add(u)

                    # Condition for Bridge: low[v] > discovery_time[u]
                    if low[v] > discovery_time[u]:
                        edge = (min(u, v), max(u, v))
                        bridges.append(edge)

            # Condition 2 for Articulation Point: Root vertex u with 2 or more children in DFS tree
            if parent[u] == -1 and children > 1:
                articulation_points.add(u)

        for i in range(self.num_vertices):
            if not visited[i]:
                dfs(i)

        bridges.sort()
        return articulation_points, bridges


def find_cut_vertices_and_edges(
    num_vertices: int, edges: List[Tuple[int, int]]
) -> Tuple[Set[int], List[Tuple[int, int]]]:
    """Convenience function to build graph and return articulation points and bridges."""
    analyzer = GraphCutAnalyzer(num_vertices)
    for u, v in edges:
        analyzer.add_edge(u, v)
    return analyzer.find_articulation_points_and_bridges()
