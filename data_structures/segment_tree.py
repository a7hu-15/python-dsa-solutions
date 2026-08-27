"""
Segment Tree Implementation in Python.

A Segment Tree is a tree data structure used for storing information about intervals
or segments. It allows querying which of the stored segments contain a given point or range queries.
Operations like range sum/min/max query and point update operate in O(log N) time complexity.

Complexity Analysis:
- Build Tree: O(N) time, O(N) space
- Query (Range Sum/Min/Max): O(log N) time
- Update (Point Update): O(log N) time
"""

from typing import List, Callable, Union

class SegmentTree:
    """
    A generic Segment Tree supporting custom binary operation functions
    such as sum (default), min, or max.

    >>> nums = [1, 3, 5, 7, 9, 11]
    >>> seg_tree = SegmentTree(nums)
    >>> seg_tree.query(1, 3)
    15
    >>> seg_tree.update(1, 10)
    >>> seg_tree.query(1, 3)
    22
    >>> min_tree = SegmentTree([5, 2, 8, 1, 9], operation=min, default_val=float('inf'))
    >>> min_tree.query(0, 4)
    1
    """

    def __init__(self, data: List[Union[int, float]], operation: Callable = sum, default_val: Union[int, float] = 0):
        self.n = len(data)
        self.operation = operation
        self.default_val = default_val
        self.tree = [default_val] * (4 * self.n)
        if self.n > 0:
            self._build(data, 0, 0, self.n - 1)

    def _combine(self, a: Union[int, float], b: Union[int, float]) -> Union[int, float]:
        if self.operation is sum:
            return a + b
        return self.operation(a, b)

    def _build(self, data: List[Union[int, float]], node: int, start: int, end: int) -> None:
        if start == end:
            self.tree[node] = data[start]
            return
        mid = (start + end) // 2
        left_node = 2 * node + 1
        right_node = 2 * node + 2
        self._build(data, left_node, start, mid)
        self._build(data, right_node, mid + 1, end)
        self.tree[node] = self._combine(self.tree[left_node], self.tree[right_node])

    def update(self, index: int, value: Union[int, float]) -> None:
        """Point update: Update element at given index to value in O(log N)."""
        if 0 <= index < self.n:
            self._update(0, 0, self.n - 1, index, value)

    def _update(self, node: int, start: int, end: int, idx: int, val: Union[int, float]) -> None:
        if start == end:
            self.tree[node] = val
            return
        mid = (start + end) // 2
        left_node = 2 * node + 1
        right_node = 2 * node + 2
        if start <= idx <= mid:
            self._update(left_node, start, mid, idx, val)
        else:
            self._update(right_node, mid + 1, end, idx, val)
        self.tree[node] = self._combine(self.tree[left_node], self.tree[right_node])

    def query(self, left: int, right: int) -> Union[int, float]:
        """Range query: Perform binary operation over range [left, right] inclusive in O(log N)."""
        if self.n == 0 or left > right or left < 0 or right >= self.n:
            return self.default_val
        return self._query(0, 0, self.n - 1, left, right)

    def _query(self, node: int, start: int, end: int, l: int, r: int) -> Union[int, float]:
        if r < start or end < l:
            return self.default_val
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        left_val = self._query(2 * node + 1, start, mid, l, r)
        right_val = self._query(2 * node + 2, mid + 1, end, l, r)
        return self._combine(left_val, right_val)


if __name__ == "__main__":
    import doctest
    results = doctest.testmod()
    if results.failed == 0:
        print(f"All {results.attempted} Segment Tree doctests passed successfully!")
