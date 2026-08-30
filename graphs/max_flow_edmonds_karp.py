"""
Edmonds-Karp Algorithm for Maximum Flow

The Edmonds-Karp algorithm is an implementation of the Ford-Fulkerson method for
computing the maximum flow in a flow network. It uses Breadth-First Search (BFS)
to find augmenting paths from the source to the sink.

Algorithm Mechanism:
    - Build a residual capacity network containing forward and backward edges.
    - Repeatedly run BFS to find the shortest augmenting path (fewest edges) from source to sink.
    - If no augmenting path exists, the current total flow is maximum.
    - Determine the bottleneck capacity (minimum capacity along augmenting path).
    - Increase flow along path: subtract capacity on forward edges, add capacity on backward edges.

Time Complexity:  O(V * E^2)
Space Complexity: O(V + E) for residual graph representation.

>>> ek = EdmondsKarp()
>>> ek.add_edge("S", "A", 10)
>>> ek.add_edge("S", "C", 10)
>>> ek.add_edge("A", "B", 4)
>>> ek.add_edge("A", "C", 2)
>>> ek.add_edge("A", "D", 8)
>>> ek.add_edge("C", "D", 9)
>>> ek.add_edge("B", "T", 10)
>>> ek.add_edge("D", "T", 10)
>>> ek.max_flow("S", "T")
14
"""

from __future__ import annotations

from collections import deque
import unittest
from typing import Dict, Generic, List, Optional, Set, Tuple, TypeVar

T = TypeVar("T")


class EdmondsKarp(Generic[T]):
    """Class representing a Flow Network and executing Edmonds-Karp Max Flow algorithm."""

    def __init__(self) -> None:
        self.graph: Dict[T, Dict[T, int]] = {}

    def add_edge(self, u: T, v: T, capacity: int) -> None:
        """
        Add a directed edge from u to v with specified capacity.
        Also initializes reverse edge with 0 capacity if not present.
        """
        if u not in self.graph:
            self.graph[u] = {}
        if v not in self.graph:
            self.graph[v] = {}

        if v not in self.graph[u]:
            self.graph[u][v] = 0
        if u not in self.graph[v]:
            self.graph[v][u] = 0

        self.graph[u][v] += capacity

    def _bfs(self, source: T, sink: T, parent: Dict[T, Optional[T]]) -> bool:
        """Find an augmenting path using BFS in the residual network."""
        visited: Set[T] = {source}
        queue: deque[T] = deque([source])

        while queue:
            curr = queue.popleft()
            if curr == sink:
                return True

            for neighbor, capacity in self.graph[curr].items():
                if neighbor not in visited and capacity > 0:
                    visited.add(neighbor)
                    parent[neighbor] = curr
                    queue.append(neighbor)

        return False

    def max_flow(self, source: T, sink: T) -> int:
        """
        Compute the maximum flow from source to sink.
        Modifies residual capacities in-place.
        """
        if source not in self.graph or sink not in self.graph:
            return 0

        max_flow_val = 0
        parent: Dict[T, Optional[T]] = {}

        while self._bfs(source, sink, parent):
            # Find bottleneck capacity along the augmenting path
            path_flow = float("inf")
            s = sink
            while s != source:
                p = parent[s]
                assert p is not None
                path_flow = min(path_flow, self.graph[p][s])
                s = p

            path_flow = int(path_flow)
            max_flow_val += path_flow

            # Update residual capacities
            v = sink
            while v != source:
                u = parent[v]
                assert u is not None
                self.graph[u][v] -= path_flow
                self.graph[v][u] += path_flow
                v = u

            parent.clear()

        return max_flow_val

    def min_cut(self, source: T) -> Set[T]:
        """
        Find reachable nodes from source in residual graph (S-side of min-cut).
        Should be called after max_flow.
        """
        visited: Set[T] = {source}
        queue: deque[T] = deque([source])

        while queue:
            curr = queue.popleft()
            for neighbor, capacity in self.graph.get(curr, {}).items():
                if neighbor not in visited and capacity > 0:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return visited


class TestEdmondsKarp(unittest.TestCase):
    def test_simple_network(self) -> None:
        ek = EdmondsKarp[str]()
        ek.add_edge("S", "A", 3)
        ek.add_edge("S", "B", 2)
        ek.add_edge("A", "B", 1)
        ek.add_edge("A", "T", 2)
        ek.add_edge("B", "T", 3)
        self.assertEqual(ek.max_flow("S", "T"), 5)

    def test_classic_example(self) -> None:
        ek = EdmondsKarp[str]()
        ek.add_edge("S", "A", 10)
        ek.add_edge("S", "C", 10)
        ek.add_edge("A", "B", 4)
        ek.add_edge("A", "C", 2)
        ek.add_edge("A", "D", 8)
        ek.add_edge("C", "D", 9)
        ek.add_edge("B", "T", 10)
        ek.add_edge("D", "T", 10)
        self.assertEqual(ek.max_flow("S", "T"), 14)

    def test_disconnected_graph(self) -> None:
        ek = EdmondsKarp[str]()
        ek.add_edge("S", "A", 10)
        ek.add_edge("B", "T", 10)
        self.assertEqual(ek.max_flow("S", "T"), 0)

    def test_min_cut(self) -> None:
        ek = EdmondsKarp[str]()
        ek.add_edge("S", "A", 10)
        ek.add_edge("A", "T", 5)
        self.assertEqual(ek.max_flow("S", "T"), 5)
        cut = ek.min_cut("S")
        self.assertIn("S", cut)
        self.assertIn("A", cut)
        self.assertNotIn("T", cut)


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    unittest.main()
