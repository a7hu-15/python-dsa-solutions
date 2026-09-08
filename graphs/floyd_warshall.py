"""
Floyd-Warshall All-Pairs Shortest Path Algorithm with Path Reconstruction and Negative Cycle Detection.

Computes the shortest distance between all pairs of vertices in a directed or undirected graph.
Handles negative edge weights and detects negative-weight cycles.

Time Complexity: O(V^3)
Space Complexity: O(V^2)
"""

from typing import List, Optional, Tuple


class FloydWarshall:
    """Computes all-pairs shortest paths using Dynamic Programming matrix updates."""

    def __init__(self, num_vertices: int):
        if num_vertices < 0:
            raise ValueError("Number of vertices cannot be negative")
        self.num_vertices = num_vertices
        self.INF = float("inf")
        self.dist: List[List[float]] = [
            [0.0 if i == j else self.INF for j in range(num_vertices)] for i in range(num_vertices)
        ]
        self.next_node: List[List[Optional[int]]] = [
            [j if i != j else None for j in range(num_vertices)] for i in range(num_vertices)
        ]

    def add_edge(self, u: int, v: int, weight: float, directed: bool = True) -> None:
        """Adds a weighted edge between u and v."""
        if not (0 <= u < self.num_vertices and 0 <= v < self.num_vertices):
            raise ValueError(f"Vertex index out of bounds [0, {self.num_vertices - 1}]")
        self.dist[u][v] = min(self.dist[u][v], weight)
        self.next_node[u][v] = v
        if not directed:
            self.dist[v][u] = min(self.dist[v][u], weight)
            self.next_node[v][u] = u

    def compute_shortest_paths(self) -> Tuple[List[List[float]], bool]:
        """
        Executes Floyd-Warshall dynamic programming algorithm.

        Returns:
            Tuple[List[List[float]], bool]:
                - Matrix of shortest path distances
                - Boolean indicating whether a negative-weight cycle was detected
        """
        n = self.num_vertices
        for k in range(n):
            for i in range(n):
                for j in range(n):
                    if self.dist[i][k] != self.INF and self.dist[k][j] != self.INF:
                        if self.dist[i][k] + self.dist[k][j] < self.dist[i][j]:
                            self.dist[i][j] = self.dist[i][k] + self.dist[k][j]
                            self.next_node[i][j] = self.next_node[i][k]

        # Negative cycle detection: dist[i][i] < 0
        has_negative_cycle = any(self.dist[i][i] < 0 for i in range(n))
        return self.dist, has_negative_cycle

    def get_path(self, u: int, v: int) -> Optional[List[int]]:
        """Reconstructs the shortest path from u to v."""
        if self.dist[u][v] == self.INF:
            return None
        path = [u]
        curr = u
        while curr != v:
            curr = self.next_node[curr][v]
            if curr is None or curr in path and curr != v:
                return None  # Cycle or invalid path
            path.append(curr)
        return path


def floyd_warshall(
    num_vertices: int, edges: List[Tuple[int, int, float]], directed: bool = True
) -> Tuple[List[List[float]], bool]:
    """
    Helper function to calculate all-pairs shortest distances.

    >>> dist, neg_cycle = floyd_warshall(3, [(0, 1, 4), (1, 2, -2), (0, 2, 5)])
    >>> dist[0][2]
    2.0
    >>> neg_cycle
    False
    """
    fw = FloydWarshall(num_vertices)
    for u, v, w in edges:
        fw.add_edge(u, v, w, directed=directed)
    return fw.compute_shortest_paths()
