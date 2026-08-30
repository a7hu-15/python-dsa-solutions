"""
Hierholzer's Algorithm for Eulerian Path and Circuit

An Eulerian Path is a trail in a finite graph that visits every edge exactly once.
An Eulerian Circuit is an Eulerian Path that starts and ends on the same vertex.

Algorithm Mechanism (Hierholzer's Algorithm for Directed Graphs):
    1. Validate degree conditions for directed graphs:
       - For Eulerian Circuit: in_degree == out_degree for every vertex.
       - For Eulerian Path: at most one vertex has out_degree - in_degree == 1 (start node),
         at most one vertex has in_degree - out_degree == 1 (end node), and all others have
         in_degree == out_degree.
    2. Maintain a recursion stack and follow unvisited edges until stuck.
    3. Pop vertices with no remaining outgoing edges and prepend them to the final circuit.
    4. Reverse path to get correct order from start node to end node.

Time Complexity:  O(V + E)
Space Complexity: O(V + E)

>>> ep = EulerianPath()
>>> ep.add_edge("A", "B")
>>> ep.add_edge("B", "C")
>>> ep.add_edge("C", "A")
>>> ep.find_eulerian_circuit()
['A', 'B', 'C', 'A']
>>> ep2 = EulerianPath()
>>> ep2.add_edge("A", "B")
>>> ep2.add_edge("B", "C")
>>> ep2.find_eulerian_path()
['A', 'B', 'C']
"""

from __future__ import annotations

from collections import defaultdict
import unittest
from typing import Dict, Generic, List, Optional, Set, TypeVar

T = TypeVar("T")


class EulerianPath(Generic[T]):
    """Class representing a graph to find Eulerian Paths and Circuits using Hierholzer's Algorithm."""

    def __init__(self) -> None:
        self.graph: Dict[T, List[T]] = defaultdict(list)
        self.in_degree: Dict[T, int] = defaultdict(int)
        self.out_degree: Dict[T, int] = defaultdict(int)
        self.vertices: Set[T] = set()
        self.num_edges: int = 0

    def add_edge(self, u: T, v: T) -> None:
        """Add a directed edge from u to v."""
        self.graph[u].append(v)
        self.out_degree[u] += 1
        self.in_degree[v] += 1
        self.vertices.add(u)
        self.vertices.add(v)
        self.num_edges += 1

    def _get_start_node(self, forced_start_node: Optional[T] = None) -> Optional[T]:
        """Find appropriate start node for Eulerian Path / Circuit."""
        if forced_start_node is not None:
            return forced_start_node

        start_node: Optional[T] = None
        start_nodes_count = 0
        end_nodes_count = 0

        for node in sorted(list(self.vertices)):
            out_d = self.out_degree[node]
            in_d = self.in_degree[node]

            if out_d - in_d == 1:
                start_nodes_count += 1
                start_node = node
            elif in_d - out_d == 1:
                end_nodes_count += 1
            elif in_d != out_d:
                return None

        if start_nodes_count == 0 and end_nodes_count == 0:
            # Eulerian Circuit exists; pick any vertex with out_degree > 0
            for node in sorted(list(self.vertices)):
                if self.out_degree[node] > 0:
                    return node
            return sorted(list(self.vertices))[0] if self.vertices else None

        if start_nodes_count == 1 and end_nodes_count == 1:
            return start_node

        return None

    def find_eulerian_path(self, start_node: Optional[T] = None) -> Optional[List[T]]:
        """
        Find an Eulerian Path visiting every edge exactly once.
        Returns list of vertices in order, or None if no Eulerian path exists.
        """
        if self.num_edges == 0:
            return []

        start = self._get_start_node(start_node)
        if start is None:
            return None

        # Copy graph adjacencies for traversal
        adj = {u: list(neighbors) for u, neighbors in self.graph.items()}
        stack: List[T] = [start]
        path: List[T] = []

        while stack:
            curr = stack[-1]
            if curr in adj and adj[curr]:
                nxt = adj[curr].pop()
                stack.append(nxt)
            else:
                path.append(stack.pop())

        path.reverse()

        # Verify all edges were visited
        if len(path) != self.num_edges + 1:
            return None

        return path

    def find_eulerian_circuit(self, start_node: Optional[T] = None) -> Optional[List[T]]:
        """
        Find an Eulerian Circuit starting and ending at the same node.
        Returns list of vertices in order, or None if no Eulerian circuit exists.
        """
        for node in self.vertices:
            if self.in_degree[node] != self.out_degree[node]:
                return None

        path = self.find_eulerian_path(start_node)
        if path and path[0] == path[-1]:
            return path
        return None


class TestEulerianPath(unittest.TestCase):
    def test_eulerian_circuit(self) -> None:
        ep = EulerianPath[str]()
        ep.add_edge("A", "B")
        ep.add_edge("B", "C")
        ep.add_edge("C", "A")
        circuit = ep.find_eulerian_circuit()
        self.assertIsNotNone(circuit)
        self.assertEqual(circuit, ["A", "B", "C", "A"])

    def test_eulerian_path_not_circuit(self) -> None:
        ep = EulerianPath[str]()
        ep.add_edge("A", "B")
        ep.add_edge("B", "C")
        path = ep.find_eulerian_path()
        self.assertEqual(path, ["A", "B", "C"])
        self.assertIsNone(ep.find_eulerian_circuit())

    def test_no_eulerian_path(self) -> None:
        ep = EulerianPath[str]()
        ep.add_edge("A", "B")
        ep.add_edge("A", "C")
        ep.add_edge("A", "D")
        self.assertIsNone(ep.find_eulerian_path())

    def test_complex_circuit(self) -> None:
        ep = EulerianPath[int]()
        # 0 -> 1 -> 2 -> 0 -> 3 -> 0
        ep.add_edge(0, 1)
        ep.add_edge(1, 2)
        ep.add_edge(2, 0)
        ep.add_edge(0, 3)
        ep.add_edge(3, 0)
        circuit = ep.find_eulerian_circuit()
        self.assertIsNotNone(circuit)
        self.assertEqual(len(circuit), 6)
        self.assertEqual(circuit[0], circuit[-1])


if __name__ == "__main__":
    import doctest
    doctest.testmod()
    unittest.main()
