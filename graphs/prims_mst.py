"""Prim's Minimum Spanning Tree (MST) Algorithm.

This module provides an efficient implementation of Prim's algorithm to find the
Minimum Spanning Tree of a connected, undirected, weighted graph using a binary min-heap.

Time Complexity:
- Prim's MST: O(E log V) using a binary min-heap / priority queue, where V is the number
  of vertices and E is the number of edges.

Space Complexity:
- O(V + E) to store the adjacency list representation of the graph and min-heap state.
"""

import heapq
from typing import Dict, List, Tuple


def prims_mst(
    num_vertices: int,
    edges: List[Tuple[int, int, int]],
    start_vertex: int = 0
) -> Tuple[int, List[Tuple[int, int, int]]]:
    """Computes the Minimum Spanning Tree (MST) of a graph using Prim's Algorithm.

    Args:
        num_vertices: Total number of vertices in the graph (0 to num_vertices - 1).
        edges: List of tuples (u, v, weight) representing undirected weighted edges.
        start_vertex: The starting vertex for Prim's algorithm (default: 0).

    Returns:
        Tuple containing total weight of the MST and list of edges (u, v, weight) included in the MST.

    Raises:
        ValueError: If num_vertices <= 0 or start_vertex is out of valid range.

    >>> edges = [(0, 1, 10), (0, 2, 6), (0, 3, 5), (1, 3, 15), (2, 3, 4)]
    >>> total_weight, mst_edges = prims_mst(4, edges)
    >>> total_weight
    19
    >>> sorted([(min(u, v), max(u, v), w) for u, v, w in mst_edges])
    [(0, 1, 10), (0, 3, 5), (2, 3, 4)]
    """
    if num_vertices <= 0:
        raise ValueError("num_vertices must be greater than 0")
    if not (0 <= start_vertex < num_vertices):
        raise ValueError(f"start_vertex {start_vertex} out of range [0, {num_vertices - 1}]")

    if num_vertices == 1:
        return 0, []

    # Build adjacency list: adj[u] = [(weight, v), ...]
    adj: Dict[int, List[Tuple[int, int]]] = {i: [] for i in range(num_vertices)}
    for u, v, weight in edges:
        adj[u].append((weight, v))
        adj[v].append((weight, u))

    visited = [False] * num_vertices
    min_heap: List[Tuple[int, int, int]] = []  # (weight, u, v)

    # Mark start vertex as visited and add all outgoing edges to min_heap
    visited[start_vertex] = True
    for weight, v in adj[start_vertex]:
        heapq.heappush(min_heap, (weight, start_vertex, v))

    mst_edges: List[Tuple[int, int, int]] = []
    total_weight = 0

    while min_heap and len(mst_edges) < num_vertices - 1:
        weight, u, v = heapq.heappop(min_heap)

        # Skip if target vertex already in MST
        if visited[v]:
            continue

        # Include edge in MST
        visited[v] = True
        mst_edges.append((u, v, weight))
        total_weight += weight

        # Push newly accessible edges from v to unvisited neighbors
        for nbr_weight, nbr in adj[v]:
            if not visited[nbr]:
                heapq.heappush(min_heap, (nbr_weight, v, nbr))

    return total_weight, mst_edges


if __name__ == "__main__":
    import doctest

    results = doctest.testmod()
    print(f"Doctest results: {results}")
