"""
Dijkstra's Shortest Path Algorithm

Dijkstra's algorithm finds the shortest path from a starting source node to all
other nodes in a weighted graph with non-negative edge weights.

Algorithm Mechanism:
    - Maintain a min-priority queue of (distance, vertex) tuples.
    - Continuously extract the vertex with the smallest distance.
    - Relax adjacent edges: if distance to neighbor via current vertex is shorter,
      update neighbor's shortest distance and push to priority queue.

Time Complexity:  O((V + E) * log V) using a binary heap (Min-Heap).
Space Complexity: O(V + E) to store graph and distance/predecessor structures.

>>> g = Graph()
>>> g.add_edge("A", "B", 4)
>>> g.add_edge("A", "C", 2)
>>> g.add_edge("B", "C", 1)
>>> g.add_edge("B", "D", 5)
>>> g.add_edge("C", "D", 8)
>>> g.add_edge("C", "E", 10)
>>> g.add_edge("D", "E", 2)
>>> distances, predecessors = dijkstra(g, "A")
>>> distances["E"]
10.0
>>> reconstruct_path(predecessors, "A", "E")
['A', 'C', 'B', 'D', 'E']
"""

from __future__ import annotations

import heapq
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class Graph(Generic[T]):
    """
    Weighted Graph implementation using Adjacency Lists.

    >>> g = Graph()
    >>> g.add_edge(1, 2, 5)
    >>> g.add_edge(2, 3, 3, directed=True)
    >>> g.get_neighbors(1)
    [(2, 5.0)]
    >>> g.get_neighbors(2)
    [(1, 5.0), (3, 3.0)]
    """

    def __init__(self) -> None:
        """Initialize an empty adjacency list graph."""
        self._adj: dict[T, list[tuple[T, float]]] = {}

    def add_vertex(self, vertex: T) -> None:
        """Add a vertex to the graph if it doesn't already exist."""
        if vertex not in self._adj:
            self._adj[vertex] = []

    def add_edge(self, u: T, v: T, weight: float, directed: bool = False) -> None:
        """
        Add a weighted edge between vertex u and vertex v.

        Args:
            u: Source vertex.
            v: Destination vertex.
            weight: Edge weight (must be non-negative).
            directed: If True, edge is u -> v. If False, edge is u <-> v.

        Raises:
            ValueError: If weight is negative.
        """
        if weight < 0:
            raise ValueError(f"Dijkstra's algorithm does not support negative edge weight: {weight}")

        self.add_vertex(u)
        self.add_vertex(v)

        self._adj[u].append((v, float(weight)))
        if not directed:
            self._adj[v].append((u, float(weight)))

    def get_vertices(self) -> list[T]:
        """Return list of all vertices in the graph."""
        return list(self._adj.keys())

    def get_neighbors(self, vertex: T) -> list[tuple[T, float]]:
        """Return adjacency list for vertex as a list of (neighbor, weight) tuples."""
        return self._adj.get(vertex, [])

    def __contains__(self, vertex: T) -> bool:
        return vertex in self._adj

    def __len__(self) -> int:
        return len(self._adj)


def dijkstra(
    graph: Graph[T], source: T
) -> tuple[dict[T, float], dict[T, T | None]]:
    """
    Compute shortest path distances and predecessors from a source node using Dijkstra's algorithm.

    Args:
        graph: Graph instance.
        source: Source node identifier.

    Returns:
        Tuple of (distances_dict, predecessors_dict).
        distances_dict: Mapping of node to shortest distance from source.
        predecessors_dict: Mapping of node to previous node on shortest path.

    Raises:
        ValueError: If source node is not in graph.

    >>> g = Graph()
    >>> g.add_edge('S', 'A', 2)
    >>> g.add_edge('S', 'B', 5)
    >>> g.add_edge('A', 'B', 1)
    >>> distances, preds = dijkstra(g, 'S')
    >>> distances['B']
    3.0
    """
    if source not in graph:
        raise ValueError(f"Source vertex '{source}' not found in graph")

    distances: dict[T, float] = {v: float("inf") for v in graph.get_vertices()}
    predecessors: dict[T, T | None] = {v: None for v in graph.get_vertices()}

    distances[source] = 0.0

    # Priority queue stores tuples of (distance, vertex)
    pq: list[tuple[float, T]] = [(0.0, source)]

    visited: set[T] = set()

    while pq:
        current_dist, current_vertex = heapq.heappop(pq)

        if current_vertex in visited:
            continue
        visited.add(current_vertex)

        for neighbor, weight in graph.get_neighbors(current_vertex):
            if neighbor in visited:
                continue

            new_dist = current_dist + weight
            if new_dist < distances[neighbor]:
                distances[neighbor] = new_dist
                predecessors[neighbor] = current_vertex
                heapq.heappush(pq, (new_dist, neighbor))

    return distances, predecessors


def reconstruct_path(
    predecessors: dict[T, T | None], source: T, target: T
) -> list[T]:
    """
    Reconstruct shortest path from source to target using predecessors dictionary.

    Returns:
        List of vertices forming the shortest path from source to target.
        Returns empty list if target is unreachable.

    >>> preds = {'A': None, 'B': 'A', 'C': 'B'}
    >>> reconstruct_path(preds, 'A', 'C')
    ['A', 'B', 'C']
    >>> reconstruct_path(preds, 'A', 'D')
    []
    """
    if target not in predecessors:
        return []

    path: list[T] = []
    curr: T | None = target

    while curr is not None:
        path.append(curr)
        if curr == source:
            break
        curr = predecessors.get(curr)

    if path and path[-1] == source:
        path.reverse()
        return path

    return []


if __name__ == "__main__":
    import doctest

    print("Running Dijkstra's Algorithm doctests...")
    results = doctest.testmod()
    if results.failed == 0:
        print(f"✅ All {results.attempted} tests passed!")
    else:
        print(f"❌ {results.failed} tests failed out of {results.attempted}")
