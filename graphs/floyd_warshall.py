"""
Floyd-Warshall All-Pairs Shortest Path Algorithm in Python.

Floyd-Warshall is a dynamic programming algorithm used to find the shortest paths
between all pairs of vertices in a weighted graph (with positive or negative edge weights),
and can detect negative-weight cycles.

Complexity Analysis:
- Time Complexity: O(V^3) where V is the number of vertices.
- Space Complexity: O(V^2) for distance and predecessor matrices.
"""

from typing import List, Tuple, Optional, Dict

INF = float("inf")


class FloydWarshall:
    """
    Floyd-Warshall All-Pairs Shortest Path implementation.

    >>> graph = [
    ...     [0, 5, INF, 10],
    ...     [INF, 0, 3, INF],
    ...     [INF, INF, 0, 1],
    ...     [INF, INF, INF, 0]
    ... ]
    >>> fw = FloydWarshall(4, graph)
    >>> dist, has_neg_cycle = fw.compute_shortest_paths()
    >>> has_neg_cycle
    False
    >>> dist[0][2]
    8
    >>> fw.reconstruct_path(0, 3)
    [0, 1, 2, 3]
    """

    def __init__(self, num_vertices: int, graph_matrix: List[List[float]]):
        self.v = num_vertices
        self.dist = [row[:] for row in graph_matrix]
        self.next_node = [[None if cell == INF or i == j else j for j, cell in enumerate(row)]
                         for i, row in enumerate(graph_matrix)]

    def compute_shortest_paths(self) -> Tuple[List[List[float]], bool]:
        """
        Compute shortest paths between all pairs of vertices.
        Returns:
            Tuple containing distance matrix and boolean indicating presence of negative cycle.
        """
        for k in range(self.v):
            for i in range(self.v):
                for j in range(self.v):
                    if self.dist[i][k] != INF and self.dist[k][j] != INF:
                        if self.dist[i][k] + self.dist[k][j] < self.dist[i][j]:
                            self.dist[i][j] = self.dist[i][k] + self.dist[k][j]
                            self.next_node[i][j] = self.next_node[i][k]

        # Check for negative-weight cycles
        has_negative_cycle = False
        for i in range(self.v):
            if self.dist[i][i] < 0:
                has_negative_cycle = True
                break

        return self.dist, has_negative_cycle

    def reconstruct_path(self, u: int, v: int) -> Optional[List[int]]:
        """
        Reconstruct shortest path from vertex u to vertex v.
        """
        if self.dist[u][v] == INF:
            return None

        path = [u]
        curr = u
        while curr != v:
            curr = self.next_node[curr][v]
            if curr is None:
                return None
            path.append(curr)

        return path


if __name__ == "__main__":
    import doctest
    results = doctest.testmod()
    if results.failed == 0:
        print(f"All {results.attempted} Floyd-Warshall doctests passed successfully!")
