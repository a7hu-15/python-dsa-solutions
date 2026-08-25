"""
Topological Sort Implementation (Kahn's Algorithm & DFS approach)
------------------------------------------------------------------
Topological sorting for Directed Acyclic Graphs (DAG).
Provides both BFS (Kahn's Algorithm using in-degrees) and DFS-based implementations.
"""

from collections import deque, defaultdict
from typing import List, Dict, Set

class GraphTopologicalSort:
    def __init__(self, vertices: int):
        self.vertices = vertices
        self.adj_list: Dict[int, List[int]] = defaultdict(list)
        self.in_degree: Dict[int, int] = {i: 0 for i in range(vertices)}

    def add_edge(self, u: int, v: int) -> None:
        """Add a directed edge from vertex u to vertex v."""
        self.adj_list[u].append(v)
        self.in_degree[v] += 1

    def kahns_topological_sort(self) -> List[int]:
        """
        Computes topological ordering using Kahn's Algorithm (BFS).
        Returns an empty list if a cycle is detected.
        """
        queue = deque([v for v in range(self.vertices) if self.in_degree[v] == 0])
        topo_order = []

        # Local copy of in-degrees
        in_degrees = self.in_degree.copy()

        while queue:
            node = queue.popleft()
            topo_order.append(node)

            for neighbor in self.adj_list[node]:
                in_degrees[neighbor] -= 1
                if in_degrees[neighbor] == 0:
                    queue.append(neighbor)

        if len(topo_order) != self.vertices:
            return []  # Cycle detected

        return topo_order

    def dfs_topological_sort(self) -> List[int]:
        """
        Computes topological ordering using DFS.
        Returns empty list if a cycle is detected.
        """
        visited: Set[int] = set()
        rec_stack: Set[int] = set()
        stack: List[int] = []

        def dfs(v: int) -> bool:
            visited.add(v)
            rec_stack.add(v)

            for neighbor in self.adj_list[v]:
                if neighbor not in visited:
                    if not dfs(neighbor):
                        return False
                elif neighbor in rec_stack:
                    return False  # Cycle detected

            rec_stack.remove(v)
            stack.append(v)
            return True

        for i in range(self.vertices):
            if i not in visited:
                if not dfs(i):
                    return []  # Cycle found

        return stack[::-1]


def test_topological_sort():
    g = GraphTopologicalSort(6)
    g.add_edge(5, 2)
    g.add_edge(5, 0)
    g.add_edge(4, 0)
    g.add_edge(4, 1)
    g.add_edge(2, 3)
    g.add_edge(3, 1)

    kahn_res = g.kahns_topological_sort()
    dfs_res = g.dfs_topological_sort()

    print("Kahn's Topological Order:", kahn_res)
    print("DFS Topological Order:", dfs_res)
    assert len(kahn_res) == 6, "Kahn's sort should process all 6 vertices"
    assert len(dfs_res) == 6, "DFS sort should process all 6 vertices"
    print("All Topological Sort tests passed!")

if __name__ == "__main__":
    test_topological_sort()
