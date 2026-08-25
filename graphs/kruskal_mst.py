"""Disjoint Set Union (DSU) & Kruskal's Minimum Spanning Tree (MST) Algorithm.

This module provides an efficient implementation of the Disjoint Set Union
(Union-Find) data structure with Path Compression and Union by Rank, along
with Kruskal's algorithm to compute the Minimum Spanning Tree of a weighted graph.

Time Complexity:
- DisjointSet Find / Union: O(alpha(V)) where alpha is the inverse Ackermann function (effectively O(1)).
- Kruskal's MST: O(E log E) or O(E log V) where E is number of edges and V is number of vertices.

Space Complexity:
- O(V) for parent and rank arrays in DisjointSet.
"""

from typing import List, Tuple


class DisjointSet:
    """Disjoint Set Union (DSU) data structure with path compression and union by rank.

    >>> dsu = DisjointSet(5)
    >>> dsu.union(0, 1)
    True
    >>> dsu.union(1, 2)
    True
    >>> dsu.connected(0, 2)
    True
    >>> dsu.connected(0, 3)
    False
    >>> dsu.union(0, 2)  # Already in same set
    False
    """

    def __init__(self, size: int) -> None:
        self.parent = list(range(size))
        self.rank = [0] * size
        self.num_sets = size

    def find(self, i: int) -> int:
        """Finds the representative of the set containing element i with path compression."""
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])
        return self.parent[i]

    def union(self, i: int, j: int) -> bool:
        """Unites the sets containing elements i and j using union by rank.

        Returns True if elements were in different sets and successfully merged, False otherwise.
        """
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i == root_j:
            return False

        if self.rank[root_i] < self.rank[root_j]:
            self.parent[root_i] = root_j
        elif self.rank[root_i] > self.rank[root_j]:
            self.parent[root_j] = root_i
        else:
            self.parent[root_j] = root_i
            self.rank[root_i] += 1

        self.num_sets -= 1
        return True

    def connected(self, i: int, j: int) -> bool:
        """Returns True if elements i and j belong to the same set."""
        return self.find(i) == self.find(j)


def kruskal_mst(num_vertices: int, edges: List[Tuple[int, int, int]]) -> Tuple[int, List[Tuple[int, int, int]]]:
    """Computes the Minimum Spanning Tree (MST) of a weighted graph using Kruskal's Algorithm.

    Args:
        num_vertices: Total number of vertices in the graph (0 to num_vertices - 1).
        edges: List of tuples (u, v, weight) representing undirected weighted edges.

    Returns:
        Tuple containing total weight of the MST and list of edges included in the MST.

    >>> edges = [(0, 1, 10), (0, 2, 6), (0, 3, 5), (1, 3, 15), (2, 3, 4)]
    >>> total_weight, mst_edges = kruskal_mst(4, edges)
    >>> total_weight
    19
    >>> sorted(mst_edges)
    [(0, 1, 10), (0, 3, 5), (2, 3, 4)]
    """
    if num_vertices <= 0:
        return 0, []

    # Sort edges in ascending order of weight
    sorted_edges = sorted(edges, key=lambda edge: edge[2])

    dsu = DisjointSet(num_vertices)
    mst_edges: List[Tuple[int, int, int]] = []
    total_weight = 0

    for u, v, weight in sorted_edges:
        if dsu.union(u, v):
            mst_edges.append((u, v, weight))
            total_weight += weight
            if len(mst_edges) == num_vertices - 1:
                break

    return total_weight, mst_edges


if __name__ == "__main__":
    import doctest

    results = doctest.testmod()
    print(f"Doctest results: {results}")
