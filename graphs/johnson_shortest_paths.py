"""
Johnson's Algorithm for All-Pairs Shortest Paths in Weighted Directed Graphs.

Johnson's algorithm finds the shortest paths between all pairs of vertices in a sparse,
weighted, directed graph. It allows some edge weights to be negative numbers, but no
negative-weight cycles can exist.

It operates by:
1. Adding a new vertex q connected by 0-weight directed edges to all other vertices.
2. Running the Bellman-Ford algorithm starting from q to compute vertex potentials h(v).
   If a negative-weight cycle is detected, the algorithm terminates.
3. Reweighting edge weights: w'(u, v) = w(u, v) + h(u) - h(v) >= 0.
4. Running Dijkstra's algorithm from each vertex u using the non-negative reweighted edges.
5. Converting reweighted distances back to true shortest path distances:
   dist(u, v) = dist'(u, v) - h(u) + h(v).

Time Complexity: O(V^2 log V + V * E) using Fibonacci / binary heap Dijkstra
Space Complexity: O(V^2) for distance matrix / O(V + E) for graph storage
"""

import heapq
import math
from typing import Dict, List, Tuple, Optional


class JohnsonShortestPaths:
    """Finds all-pairs shortest paths in a weighted directed graph using Johnson's Algorithm."""

    def __init__(self, num_vertices: int):
        if num_vertices <= 0:
            raise ValueError("Number of vertices must be positive")
        self.num_vertices = num_vertices
        self.adj_list: Dict[int, List[Tuple[int, float]]] = {i: [] for i in range(num_vertices)}
        self.edges: List[Tuple[int, int, float]] = []

    def add_edge(self, u: int, v: int, weight: float) -> None:
        """
        Adds a directed edge from u to v with specified weight.

        Args:
            u: Source vertex index (0-indexed)
            v: Destination vertex index (0-indexed)
            weight: Edge weight (can be negative, positive, or zero)
        """
        if not (0 <= u < self.num_vertices and 0 <= v < self.num_vertices):
            raise ValueError(f"Vertex indices out of bounds [0, {self.num_vertices - 1}]")
        self.adj_list[u].append((v, weight))
        self.edges.append((u, v, weight))

    def _bellman_ford(self, src: int, extended_edges: List[Tuple[int, int, float]], total_nodes: int) -> Optional[List[float]]:
        """Runs Bellman-Ford to compute potential values h for reweighting."""
        dist = [math.inf] * total_nodes
        dist[src] = 0.0

        for _ in range(total_nodes - 1):
            updated = False
            for u, v, w in extended_edges:
                if dist[u] != math.inf and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    updated = True
            if not updated:
                break

        # Check for negative-weight cycles
        for u, v, w in extended_edges:
            if dist[u] != math.inf and dist[u] + w < dist[v]:
                return None  # Negative cycle detected

        return dist

    def _dijkstra(self, src: int, reweighted_adj: Dict[int, List[Tuple[int, float]]]) -> List[float]:
        """Runs Dijkstra's algorithm on non-negative reweighted edges from source vertex src."""
        dist = [math.inf] * self.num_vertices
        dist[src] = 0.0
        pq: List[Tuple[float, int]] = [(0.0, src)]

        while pq:
            d, u = heapq.heappop(pq)
            if d > dist[u]:
                continue

            for v, weight in reweighted_adj[u]:
                if dist[u] + weight < dist[v]:
                    dist[v] = dist[u] + weight
                    heapq.heappush(pq, (dist[v], v))

        return dist

    def compute_all_pairs_shortest_paths(self) -> List[List[float]]:
        """
        Computes shortest path distances between all pairs of vertices.

        Returns:
            List[List[float]]: 2D matrix of shape (num_vertices, num_vertices) where
            matrix[u][v] is the shortest distance from vertex u to vertex v.
            Returns math.inf if v is unreachable from u.

        Raises:
            ValueError: If the graph contains a negative-weight cycle.
        """
        # Step 1 & 2: Add virtual vertex q (index = self.num_vertices)
        q = self.num_vertices
        extended_edges = list(self.edges)
        for u in range(self.num_vertices):
            extended_edges.append((q, u, 0.0))

        h = self._bellman_ford(q, extended_edges, self.num_vertices + 1)
        if h is None:
            raise ValueError("Graph contains a negative-weight cycle")

        # Step 3: Reweight edges w'(u, v) = w(u, v) + h[u] - h[v]
        reweighted_adj: Dict[int, List[Tuple[int, float]]] = {i: [] for i in range(self.num_vertices)}
        for u in range(self.num_vertices):
            for v, w in self.adj_list[u]:
                reweighted_w = w + h[u] - h[v]
                reweighted_adj[u].append((v, reweighted_w))

        # Step 4 & 5: Run Dijkstra for each vertex and restore original distances
        distance_matrix: List[List[float]] = []

        for u in range(self.num_vertices):
            dijkstra_dist = self._dijkstra(u, reweighted_adj)
            row: List[float] = []
            for v in range(self.num_vertices):
                if dijkstra_dist[v] == math.inf:
                    row.append(math.inf)
                else:
                    # dist(u, v) = dist'(u, v) - h[u] + h[v]
                    true_dist = dijkstra_dist[v] - h[u] + h[v]
                    row.append(round(true_dist, 10))
            distance_matrix.append(row)

        return distance_matrix
