"""
Tarjan's Strongly Connected Components (SCC) Algorithm in Python.

Tarjan's algorithm is a linear-time algorithm to find all strongly connected components
in a directed graph. A strongly connected component is a maximal subgraph where every
vertex is reachable from every other vertex in the component.

Complexity Analysis:
- Time Complexity: O(V + E)
- Space Complexity: O(V)
"""

from typing import List, Dict


class TarjanSCC:
    """
    Finds Strongly Connected Components (SCC) using Tarjan's algorithm.

    >>> graph = {
    ...     0: [1],
    ...     1: [2],
    ...     2: [0, 3],
    ...     3: [4],
    ...     4: [5, 6],
    ...     5: [3],
    ...     6: []
    ... }
    >>> solver = TarjanSCC(7, graph)
    >>> sccs = solver.get_sccs()
    >>> sccs
    [[6], [5, 4, 3], [2, 1, 0]]
    """

    def __init__(self, num_vertices: int, graph: Dict[int, List[int]]):
        self.v = num_vertices
        self.graph = graph
        self.index = 0
        self.stack: List[int] = []
        self.on_stack = [False] * self.v
        self.indices = [-1] * self.v
        self.low_link = [-1] * self.v
        self.sccs: List[List[int]] = []

    def get_sccs(self) -> List[List[int]]:
        """
        Compute and return list of strongly connected components.
        """
        for i in range(self.v):
            if self.indices[i] == -1:
                self._strong_connect(i)
        return self.sccs

    def _strong_connect(self, u: int) -> None:
        self.indices[u] = self.index
        self.low_link[u] = self.index
        self.index += 1
        self.stack.append(u)
        self.on_stack[u] = True

        for v in self.graph.get(u, []):
            if self.indices[v] == -1:
                self._strong_connect(v)
                self.low_link[u] = min(self.low_link[u], self.low_link[v])
            elif self.on_stack[v]:
                self.low_link[u] = min(self.low_link[u], self.indices[v])

        if self.low_link[u] == self.indices[u]:
            scc = []
            while True:
                w = self.stack.pop()
                self.on_stack[w] = False
                scc.append(w)
                if w == u:
                    break
            self.sccs.append(scc)


if __name__ == "__main__":
    import doctest
    results = doctest.testmod()
    if results.failed == 0:
        print(f"All {results.attempted} Tarjan's SCC doctests passed successfully!")
