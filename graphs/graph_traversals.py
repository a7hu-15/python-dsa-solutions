"""
Graph Traversals & Analysis Algorithms (BFS, DFS, Connected Components, Cycle Detection)

Graph traversal algorithms systematically visit all vertices in a graph.
    - BFS (Breadth-First Search): Explores neighbors level by level using a Queue (FIFO).
      Useful for finding shortest paths in unweighted graphs.
    - DFS (Depth-First Search): Explores as deep as possible along each branch before backtracking using a Stack / Recursion (LIFO).
      Useful for topological sorting, cycle detection, and maze solving.

Complexity:
    - BFS: Time O(V + E), Space O(V)
    - DFS: Time O(V + E), Space O(V)
    - Connected Components: Time O(V + E), Space O(V)
    - Cycle Detection: Time O(V + E), Space O(V)

>>> g = GraphTraversals(directed=False)
>>> g.add_edge(0, 1)
>>> g.add_edge(0, 2)
>>> g.add_edge(1, 3)
>>> g.add_edge(2, 4)
>>> g.bfs(0)
[0, 1, 2, 3, 4]
>>> g.dfs_iterative(0)
[0, 1, 3, 2, 4]
>>> g.dfs_recursive(0)
[0, 1, 3, 2, 4]
>>> g.connected_components()
[{0, 1, 2, 3, 4}]
>>> g.has_cycle()
False
>>> g.add_edge(3, 4)
>>> g.has_cycle()
True
"""

from __future__ import annotations

from collections import deque
from typing import Dict, List, Set, TypeVar

T = TypeVar("T")


class GraphTraversals:
    """
    Graph implementation supporting BFS, DFS (iterative and recursive),
    connected component analysis, and cycle detection.
    """

    def __init__(self, directed: bool = False) -> None:
        """
        Initialize graph.

        Args:
            directed: If True, graph is directed (u -> v). If False, undirected (u <-> v).
        """
        self.directed: bool = directed
        self.adj: Dict[T, List[T]] = {}

    def add_vertex(self, vertex: T) -> None:
        """Add a vertex to the graph."""
        if vertex not in self.adj:
            self.adj[vertex] = []

    def add_edge(self, u: T, v: T) -> None:
        """
        Add an edge between vertex u and vertex v.

        >>> g = GraphTraversals()
        >>> g.add_edge("A", "B")
        >>> "A" in g.adj and "B" in g.adj
        True
        """
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u].append(v)
        if not self.directed:
            self.adj[v].append(u)

    def bfs(self, start: T) -> List[T]:
        """
        Perform Breadth-First Search (BFS) starting from given vertex.

        Returns:
            List of vertices in BFS traversal order.

        >>> g = GraphTraversals(directed=False)
        >>> g.add_edge(1, 2)
        >>> g.add_edge(1, 3)
        >>> g.add_edge(2, 4)
        >>> g.bfs(1)
        [1, 2, 3, 4]
        """
        if start not in self.adj:
            return []

        visited: Set[T] = {start}
        queue: deque[T] = deque([start])
        traversal: List[T] = []

        while queue:
            vertex = queue.popleft()
            traversal.append(vertex)

            for neighbor in self.adj.get(vertex, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        return traversal

    def dfs_iterative(self, start: T) -> List[T]:
        """
        Perform Depth-First Search (DFS) iteratively starting from given vertex.

        Returns:
            List of vertices in DFS traversal order.

        >>> g = GraphTraversals(directed=False)
        >>> g.add_edge(1, 2)
        >>> g.add_edge(1, 3)
        >>> g.dfs_iterative(1)
        [1, 2, 3]
        """
        if start not in self.adj:
            return []

        visited: Set[T] = set()
        stack: List[T] = [start]
        traversal: List[T] = []

        while stack:
            vertex = stack.pop()
            if vertex not in visited:
                visited.add(vertex)
                traversal.append(vertex)
                # Push neighbors in reverse order to visit left-to-right
                for neighbor in reversed(self.adj.get(vertex, [])):
                    if neighbor not in visited:
                        stack.append(neighbor)

        return traversal

    def dfs_recursive(self, start: T) -> List[T]:
        """
        Perform Depth-First Search (DFS) recursively starting from given vertex.

        Returns:
            List of vertices in recursive DFS traversal order.

        >>> g = GraphTraversals(directed=False)
        >>> g.add_edge(1, 2)
        >>> g.add_edge(1, 3)
        >>> g.dfs_recursive(1)
        [1, 2, 3]
        """
        if start not in self.adj:
            return []

        visited: Set[T] = set()
        traversal: List[T] = []

        def _dfs(v: T) -> None:
            visited.add(v)
            traversal.append(v)
            for neighbor in self.adj.get(v, []):
                if neighbor not in visited:
                    _dfs(neighbor)

        _dfs(start)
        return traversal

    def connected_components(self) -> List[Set[T]]:
        """
        Find all connected components in an undirected graph.

        Returns:
            List of sets, each set containing vertices of a component.

        >>> g = GraphTraversals(directed=False)
        >>> g.add_edge(1, 2)
        >>> g.add_edge(3, 4)
        >>> comps = g.connected_components()
        >>> len(comps)
        2
        """
        visited: Set[T] = set()
        components: List[Set[T]] = []

        for vertex in self.adj:
            if vertex not in visited:
                component_vertices = set(self.bfs(vertex))
                visited.update(component_vertices)
                components.append(component_vertices)

        return components

    def has_cycle(self) -> bool:
        """
        Detect if the graph contains any cycle.

        Returns:
            True if cycle exists, False otherwise.

        >>> g1 = GraphTraversals(directed=False)
        >>> g1.add_edge(1, 2)
        >>> g1.add_edge(2, 3)
        >>> g1.has_cycle()
        False
        >>> g1.add_edge(3, 1)
        >>> g1.has_cycle()
        True
        """
        visited: Set[T] = set()

        if not self.directed:
            # Undirected graph cycle detection using DFS
            def _has_cycle_undirected(v: T, parent: T | None) -> bool:
                visited.add(v)
                for neighbor in self.adj.get(v, []):
                    if neighbor not in visited:
                        if _has_cycle_undirected(neighbor, v):
                            return True
                    elif neighbor != parent:
                        return True
                return False

            for vertex in self.adj:
                if vertex not in visited:
                    if _has_cycle_undirected(vertex, None):
                        return True
            return False

        else:
            # Directed graph cycle detection using recursion stack
            rec_stack: Set[T] = set()

            def _has_cycle_directed(v: T) -> bool:
                visited.add(v)
                rec_stack.add(v)

                for neighbor in self.adj.get(v, []):
                    if neighbor not in visited:
                        if _has_cycle_directed(neighbor):
                            return True
                    elif neighbor in rec_stack:
                        return True

                rec_stack.remove(v)
                return False

            for vertex in self.adj:
                if vertex not in visited:
                    if _has_cycle_directed(vertex):
                        return True
            return False


if __name__ == "__main__":
    import doctest

    print("Running Graph Traversals doctests...")
    results = doctest.testmod()
    if results.failed == 0:
        print(f"✅ All {results.attempted} tests passed!")
    else:
        print(f"❌ {results.failed} tests failed out of {results.attempted}")
