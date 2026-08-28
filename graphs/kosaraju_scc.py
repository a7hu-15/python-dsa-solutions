"""
Kosaraju's Algorithm for Strongly Connected Components (SCC) in Directed Graphs.

A Strongly Connected Component (SCC) of a directed graph is a maximal subgraph where
every vertex is reachable from every other vertex in the component.

Kosaraju's Algorithm works in two DFS passes:
1. Perform DFS on the original graph and push vertices to a stack based on their finish times.
2. Reverse (transpose) all edges in the directed graph.
3. Pop vertices from the stack and perform DFS on the transposed graph. Each traversal
   yields one Strongly Connected Component.

Complexity Analysis:
- Time Complexity: O(V + E) for two complete DFS traversals and graph transpose.
- Space Complexity: O(V + E) to store adjacency list and transposed graph.
"""

from collections import defaultdict
from typing import Dict, List, Set, TypeVar, Generic

T = TypeVar("T")


class KosarajuSCC(Generic[T]):
    """
    Kosaraju's Algorithm solver for Strongly Connected Components.
    """

    def __init__(self):
        self.adj: Dict[T, List[T]] = defaultdict(list)
        self.vertices: Set[T] = set()

    def add_edge(self, u: T, v: T) -> None:
        """
        Add a directed edge from vertex `u` to vertex `v`.

        :param u: Source vertex.
        :param v: Destination vertex.
        """
        self.adj[u].append(v)
        self.vertices.add(u)
        self.vertices.add(v)

    def add_vertex(self, u: T) -> None:
        """Add an isolated vertex to the graph."""
        self.vertices.add(u)

    def _get_transpose(self) -> Dict[T, List[T]]:
        """Compute transposed (reversed) adjacency graph."""
        transpose: Dict[T, List[T]] = defaultdict(list)
        for u in self.vertices:
            for v in self.adj[u]:
                transpose[v].append(u)
        return transpose

    def _fill_order(self, v: T, visited: Set[T], stack: List[T]) -> None:
        """First DFS pass: populate stack in order of vertex finishing times."""
        visited.add(v)
        for neighbor in self.adj[v]:
            if neighbor not in visited:
                self._fill_order(neighbor, visited, stack)
        stack.append(v)

    def _dfs_transpose(self, v: T, visited: Set[T], component: List[T], transpose: Dict[T, List[T]]) -> None:
        """Second DFS pass: collect vertices in the current SCC."""
        visited.add(v)
        component.append(v)
        for neighbor in transpose[v]:
            if neighbor not in visited:
                self._dfs_transpose(neighbor, visited, component, transpose)

    def get_sccs(self) -> List[List[T]]:
        """
        Find all Strongly Connected Components in the directed graph.

        :return: List of components, where each component is a list of vertices.
        """
        stack: List[T] = []
        visited: Set[T] = set()

        # Step 1: Order vertices by finishing time
        for v in self.vertices:
            if v not in visited:
                self._fill_order(v, visited, stack)

        # Step 2: Compute graph transpose
        transpose = self._get_transpose()

        # Step 3: Process all vertices in order defined by stack
        visited.clear()
        sccs: List[List[T]] = []

        while stack:
            v = stack.pop()
            if v not in visited:
                component: List[T] = []
                self._dfs_transpose(v, visited, component, transpose)
                sccs.append(component)

        return sccs


if __name__ == "__main__":
    import unittest

    class TestKosarajuSCC(unittest.TestCase):
        def test_standard_scc(self):
            graph = KosarajuSCC[int]()
            # Component 1: 0 -> 1 -> 2 -> 0
            graph.add_edge(0, 1)
            graph.add_edge(1, 2)
            graph.add_edge(2, 0)

            # Edges connecting components: 2 -> 3 -> 4
            graph.add_edge(2, 3)
            graph.add_edge(3, 4)

            sccs = graph.get_sccs()
            # Expect 3 components: {0, 1, 2}, {3}, {4}
            self.assertEqual(len(sccs), 3)

            # Sort internal components for deterministic assertion
            scc_sets = [set(comp) for comp in sccs]
            self.assertIn({0, 1, 2}, scc_sets)
            self.assertIn({3}, scc_sets)
            self.assertIn({4}, scc_sets)

        def test_single_component_cycle(self):
            graph = KosarajuSCC[str]()
            graph.add_edge("A", "B")
            graph.add_edge("B", "C")
            graph.add_edge("C", "A")

            sccs = graph.get_sccs()
            self.assertEqual(len(sccs), 1)
            self.assertEqual(set(sccs[0]), {"A", "B", "C"})

        def test_disconnected_graph(self):
            graph = KosarajuSCC[int]()
            graph.add_vertex(1)
            graph.add_vertex(2)
            graph.add_vertex(3)

            sccs = graph.get_sccs()
            self.assertEqual(len(sccs), 3)

    unittest.main()
