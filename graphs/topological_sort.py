"""
Topological Sorting Algorithms for Directed Acyclic Graphs (DAGs).

Topological sorting for a Directed Acyclic Graph (DAG) is a linear ordering of vertices
such that for every directed edge u -> v, vertex u comes before v in the ordering.

This module provides two classic implementations:
1. Kahn's Algorithm (BFS based on in-degrees)
2. Depth First Search (DFS based on post-order traversal with cycle detection)

Complexity Analysis:
- Time Complexity: O(V + E) where V is the number of vertices and E is the number of edges.
- Space Complexity: O(V + E) for adjacency list representation and queue/recursion stack.
"""

from collections import deque, defaultdict
from typing import Dict, List, Set, Tuple

def topological_sort_kahn(num_vertices: int, edges: List[Tuple[int, int]]) -> List[int]:
    """
    Performs Topological Sort on a DAG using Kahn's Algorithm (BFS).

    Raises ValueError if a cycle is detected in the graph.

    >>> edges = [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]
    >>> result = topological_sort_kahn(6, edges)
    >>> # Verify edge ordering: u must appear before v for all (u, v) in edges
    >>> pos = {v: i for i, v in enumerate(result)}
    >>> all(pos[u] < pos[v] for u, v in edges)
    True
    """
    adj = defaultdict(list)
    in_degree = {i: 0 for i in range(num_vertices)}

    for u, v in edges:
        adj[u].append(v)
        in_degree[v] += 1

    queue = deque([v for v in range(num_vertices) if in_degree[v] == 0])
    topo_order = []

    while queue:
        u = queue.popleft()
        topo_order.append(u)

        for v in adj[u]:
            in_degree[v] -= 1
            if in_degree[v] == 0:
                queue.append(v)

    if len(topo_order) != num_vertices:
        raise ValueError("Graph contains a cycle; Topological Sort is impossible.")

    return topo_order


def topological_sort_dfs(num_vertices: int, edges: List[Tuple[int, int]]) -> List[int]:
    """
    Performs Topological Sort on a DAG using Depth First Search (DFS).

    Raises ValueError if a cycle is detected in the graph.

    >>> edges = [(5, 2), (5, 0), (4, 0), (4, 1), (2, 3), (3, 1)]
    >>> result = topological_sort_dfs(6, edges)
    >>> pos = {v: i for i, v in enumerate(result)}
    >>> all(pos[u] < pos[v] for u, v in edges)
    True
    """
    adj = defaultdict(list)
    for u, v in edges:
        adj[u].append(v)

    # 0 = unvisited, 1 = visiting (in current DFS path), 2 = visited
    state = [0] * num_vertices
    stack: List[int] = []

    def dfs(u: int):
        state[u] = 1  # visiting
        for v in adj[u]:
            if state[v] == 1:
                raise ValueError("Graph contains a cycle; Topological Sort is impossible.")
            if state[v] == 0:
                dfs(v)
        state[u] = 2  # visited
        stack.append(u)

    for i in range(num_vertices):
        if state[i] == 0:
            dfs(i)

    return stack[::-1]


if __name__ == "__main__":
    import doctest
    results = doctest.testmod()
    if results.failed == 0:
        print(f"All {results.attempted} Topological Sort doctests passed successfully!")
