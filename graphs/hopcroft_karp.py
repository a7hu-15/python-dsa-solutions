"""
Hopcroft-Karp Algorithm for Maximum Bipartite Matching

The Hopcroft-Karp algorithm finds a maximum cardinality matching in a bipartite graph.
It improves upon the Ford-Fulkerson augmentation approach by using BFS to find multiple
shortest augmenting paths simultaneously in each phase, followed by DFS to augment the matching.

Algorithm Mechanism:
    1. Divide vertices into two disjoint sets: Left (U) and Right (V).
    2. Phase 1 (BFS): Build a layered graph starting from unmatched vertices in U.
       Find the shortest path distance to unmatched vertices in V.
    3. Phase 2 (DFS): Find vertex-disjoint augmenting paths using the BFS distance layers.
    4. Repeat until no augmenting paths can be found.

Time Complexity:  O(E * sqrt(V))
Space Complexity: O(V + E)

>>> hk = HopcroftKarp[str, str]()
>>> hk.add_edge("u1", "v1")
>>> hk.add_edge("u1", "v2")
>>> hk.add_edge("u2", "v2")
>>> hk.add_edge("u3", "v3")
>>> hk.maximum_matching()
3
>>> sorted(hk.get_matching_pairs())
[('u1', 'v1'), ('u2', 'v2'), ('u3', 'v3')]
"""

from __future__ import annotations

from collections import defaultdict, deque
import unittest
from typing import Dict, Generic, List, Optional, Set, Tuple, TypeVar

U = TypeVar("U")  # Left partition vertex type
V = TypeVar("V")  # Right partition vertex type

NIL = None


class HopcroftKarp(Generic[U, V]):
    """Class representing a bipartite graph for finding maximum matching via Hopcroft-Karp algorithm."""

    def __init__(self) -> None:
        self.adj: Dict[U, List[V]] = defaultdict(list)
        self.left_vertices: Set[U] = set()
        self.right_vertices: Set[V] = set()
        self.pair_u: Dict[U, Optional[V]] = {}
        self.pair_v: Dict[V, Optional[U]] = {}
        self.dist: Dict[Optional[U], int] = {}

    def add_edge(self, u: U, v: V) -> None:
        """Add an undirected edge between left vertex u and right vertex v."""
        self.adj[u].append(v)
        self.left_vertices.add(u)
        self.right_vertices.add(v)

    def _bfs(self) -> bool:
        """
        BFS phase to build distance layers for augmenting paths.
        Returns True if an augmenting path to an unmatched right vertex is found.
        """
        queue: deque[Optional[U]] = deque()

        for u in self.left_vertices:
            if self.pair_u[u] is NIL:
                self.dist[u] = 0
                queue.append(u)
            else:
                self.dist[u] = float("inf")  # type: ignore[assignment]

        self.dist[NIL] = float("inf")  # type: ignore[assignment]

        while queue:
            u = queue.popleft()
            if u is not NIL and self.dist[u] < self.dist[NIL]:
                for v in self.adj[u]:
                    u_next = self.pair_v[v]
                    if self.dist[u_next] == float("inf"):
                        self.dist[u_next] = self.dist[u] + 1
                        queue.append(u_next)

        return self.dist[NIL] != float("inf")

    def _dfs(self, u: Optional[U]) -> bool:
        """
        DFS phase to find vertex-disjoint augmenting paths along distance layers.
        """
        if u is not NIL:
            for v in self.adj[u]:
                u_next = self.pair_v[v]
                if self.dist[u_next] == self.dist[u] + 1:
                    if self._dfs(u_next):
                        self.pair_v[v] = u
                        self.pair_u[u] = v
                        return True
            self.dist[u] = float("inf")  # type: ignore[assignment]
            return False
        return True

    def maximum_matching(self) -> int:
        """
        Computes the maximum matching size in the bipartite graph.
        Returns total number of matched pairs.
        """
        # Initialize matching pairs
        self.pair_u = {u: NIL for u in self.left_vertices}
        self.pair_v = {v: NIL for v in self.right_vertices}
        self.dist = {}

        matching_size = 0

        while self._bfs():
            for u in sorted(list(self.left_vertices), key=lambda x: str(x)):
                if self.pair_u[u] is NIL:
                    if self._dfs(u):
                        matching_size += 1

        return matching_size

    def get_matching_pairs(self) -> List[Tuple[U, V]]:
        """
        Returns list of matched (left, right) vertex tuples.
        Must call maximum_matching() first or computes it automatically.
        """
        if not self.pair_u:
            self.maximum_matching()

        return [(u, v) for u, v in self.pair_u.items() if v is not NIL]


class TestHopcroftKarp(unittest.TestCase):
    def test_simple_bipartite_matching(self) -> None:
        hk = HopcroftKarp[str, str]()
        hk.add_edge("u1", "v1")
        hk.add_edge("u1", "v2")
        hk.add_edge("u2", "v1")
        hk.add_edge("u3", "v2")
        hk.add_edge("u3", "v3")

        match_count = hk.maximum_matching()
        self.assertEqual(match_count, 3)
        matching = hk.get_matching_pairs()
        self.assertEqual(len(matching), 3)

    def test_disconnected_bipartite_graph(self) -> None:
        hk = HopcroftKarp[int, int]()
        hk.add_edge(1, 10)
        hk.add_edge(2, 20)
        hk.add_edge(3, 30)

        match_count = hk.maximum_matching()
        self.assertEqual(match_count, 3)
        self.assertEqual(sorted(hk.get_matching_pairs()), [(1, 10), (2, 20), (3, 30)])

    def test_complete_bipartite_graph(self) -> None:
        hk = HopcroftKarp[int, str]()
        for u in [1, 2, 3]:
            for v in ["a", "b", "c"]:
                hk.add_edge(u, v)

        self.assertEqual(hk.maximum_matching(), 3)

    def test_unbalanced_bipartite_graph(self) -> None:
        hk = HopcroftKarp[str, str]()
        hk.add_edge("u1", "v1")
        hk.add_edge("u2", "v1")
        hk.add_edge("u3", "v1")

        self.assertEqual(hk.maximum_matching(), 1)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
    unittest.main()
