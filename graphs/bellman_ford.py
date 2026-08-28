"""
Bellman-Ford Shortest Path Algorithm in Python.

The Bellman-Ford algorithm computes single-source shortest paths in a weighted graph.
Unlike Dijkstra's algorithm, Bellman-Ford can process graphs containing negative edge weights
and can detect negative-weight cycles.

Complexity Analysis:
- Time Complexity: O(V * E)
- Space Complexity: O(V)
"""

from typing import List, Tuple, Optional, Dict

INF = float("inf")


class BellmanFord:
    """
    Bellman-Ford Single-Source Shortest Path algorithm.

    >>> edges = [
    ...     (0, 1, -1),
    ...     (0, 2, 4),
    ...     (1, 2, 3),
    ...     (1, 3, 2),
    ...     (1, 4, 2),
    ...     (3, 2, 5),
    ...     (3, 1, 1),
    ...     (4, 3, -3)
    ... ]
    >>> bf = BellmanFord(5, edges)
    >>> dist, predecessor, has_neg_cycle = bf.shortest_paths(0)
    >>> has_neg_cycle
    False
    >>> dist
    {0: 0.0, 1: -1.0, 2: 2.0, 3: -2.0, 4: 1.0}
    >>> bf.reconstruct_path(0, 3, predecessor)
    [0, 1, 4, 3]
    """

    def __init__(self, num_vertices: int, edges: List[Tuple[int, int, float]]):
        self.v = num_vertices
        self.edges = edges

    def shortest_paths(self, src: int) -> Tuple[Dict[int, float], Dict[int, Optional[int]], bool]:
        """
        Compute shortest paths from source vertex `src`.
        Returns:
            Tuple of (distances dict, predecessor dict, has_negative_cycle bool)
        """
        dist = {i: INF for i in range(self.v)}
        predecessor: Dict[int, Optional[int]] = {i: None for i in range(self.v)}
        dist[src] = 0.0

        # Relax all edges V - 1 times
        for _ in range(self.v - 1):
            for u, v, w in self.edges:
                if dist[u] != INF and dist[u] + w < dist[v]:
                    dist[v] = dist[u] + w
                    predecessor[v] = u

        # Check for negative-weight cycles
        has_negative_cycle = False
        for u, v, w in self.edges:
            if dist[u] != INF and dist[u] + w < dist[v]:
                has_negative_cycle = True
                break

        return dist, predecessor, has_negative_cycle

    @staticmethod
    def reconstruct_path(src: int, target: int, predecessor: Dict[int, Optional[int]]) -> Optional[List[int]]:
        """Reconstruct shortest path from src to target using predecessor map."""
        path = []
        curr: Optional[int] = target
        while curr is not None:
            path.append(curr)
            if curr == src:
                break
            curr = predecessor.get(curr)

        path.reverse()
        return path if path and path[0] == src else None


if __name__ == "__main__":
    import doctest
    results = doctest.testmod()
    if results.failed == 0:
        print(f"All {results.attempted} Bellman-Ford doctests passed successfully!")
