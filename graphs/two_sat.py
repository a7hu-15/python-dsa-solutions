"""
2-SAT (2-Satisfiability) Solver Implementation in Python.

The 2-SAT problem determines whether a boolean formula in 2-Conjunctive Normal Form (2-CNF)
can be satisfied (i.e. assigning True/False to variables such that every clause evaluates to True).

Formulas are expressed as clauses: (A or B) and (C or D)...
Each clause (A or B) is converted into implication edges in a directed graph:
- (not A -> B)
- (not B -> A)

Using Kosaraju's/Tarjan's Strongly Connected Components (SCC), if a variable and its negation
belong to the same SCC, the formula is unsatisfiable. Otherwise, topological sorting of SCCs
gives a valid variable truth assignment.

Complexity Analysis:
- Time Complexity: O(V + E) where V = variables, E = clauses
- Space Complexity: O(V + E) for the implication graph
"""

from typing import List, Tuple, Optional, Dict


class TwoSAT:
    """
    2-SAT Solver using implication graph and Kosaraju's SCC algorithm.

    >>> solver = TwoSAT(3) # 3 variables: 1, 2, 3
    >>> solver.add_clause(1, True, 2, True)   # (x1 or x2)
    >>> solver.add_clause(1, False, 2, True)  # (not x1 or x2)
    >>> solver.add_clause(2, False, 3, False) # (not x2 or not x3)
    >>> solver.is_satisfiable()
    True
    >>> assignment = solver.get_assignment()
    >>> assignment[2]  # x2 must be True
    True
    """

    def __init__(self, num_variables: int):
        self.num_vars = num_variables
        # Total nodes: 2 * num_vars + 1 (1-indexed variables: +v and -v)
        # Node indexing: variable v -> 2*v, not v -> 2*v + 1
        self.n = 2 * (num_variables + 1)
        self.adj: List[List[int]] = [[] for _ in range(self.n)]
        self.rev_adj: List[List[int]] = [[] for _ in range(self.n)]

    def _node(self, var: int, is_true: bool) -> int:
        """Map variable index and boolean sign to node index."""
        if is_true:
            return 2 * var
        return 2 * var + 1

    def _negate(self, node: int) -> int:
        """Get node index of the negated variable."""
        return node ^ 1

    def add_clause(self, u: int, u_sign: bool, v: int, v_sign: bool) -> None:
        """
        Add clause (u_sign u or v_sign v) to 2-CNF formula.
        Implication rules:
        - not (u_sign u) -> (v_sign v)
        - not (v_sign v) -> (u_sign u)
        """
        u_node = self._node(u, u_sign)
        v_node = self._node(v, v_sign)

        not_u = self._negate(u_node)
        not_v = self._negate(v_node)

        # Implication edges: not_u -> v_node and not_v -> u_node
        self.adj[not_u].append(v_node)
        self.adj[not_v].append(u_node)

        self.rev_adj[v_node].append(not_u)
        self.rev_adj[u_node].append(not_v)

    def is_satisfiable(self) -> bool:
        """Check if 2-CNF formula is satisfiable."""

        # Step 1: First DFS pass to get finish order
        visited = [False] * self.n
        order = []

        def dfs1(node: int):
            visited[node] = True
            for neighbor in self.adj[node]:
                if not visited[neighbor]:
                    dfs1(neighbor)
            order.append(node)

        for i in range(2, self.n):
            if not visited[i]:
                dfs1(i)

        # Step 2: Second DFS pass on transpose graph to find SCCs
        scc = [-1] * self.n
        current_scc = 0

        def dfs2(node: int, scc_id: int):
            scc[node] = scc_id
            for neighbor in self.rev_adj[node]:
                if scc[neighbor] == -1:
                    dfs2(neighbor, scc_id)

        for node in reversed(order):
            if scc[node] == -1:
                dfs2(node, current_scc)
                current_scc += 1

        self.scc = scc

        # Step 3: Check if variable v and not v belong to the same SCC
        for i in range(1, self.num_vars + 1):
            if scc[2 * i] == scc[2 * i + 1]:
                return False

        return True

    def get_assignment(self) -> Dict[int, bool]:
        """
        Extract valid variable assignment dictionary if formula is satisfiable.
        Returns empty dict if unsatisfiable.
        """
        if not self.is_satisfiable():
            return {}

        assignment = {}
        for i in range(1, self.num_vars + 1):
            assignment[i] = self.scc[2 * i] > self.scc[2 * i + 1]

        return assignment


if __name__ == "__main__":
    import doctest

    results = doctest.testmod()
    if results.failed == 0:
        print(f"All {results.attempted} 2-SAT doctests passed successfully!")
