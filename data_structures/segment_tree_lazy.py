"""
Segment Tree with Lazy Propagation Implementation in Python.

A Segment Tree with Lazy Propagation allows both point/range updates and range queries
(e.g., range sum, range minimum, range maximum) in O(log N) time per operation.

Without lazy propagation, updating a range [L, R] takes O(N log N) time because
every leaf in the range must be updated individually. Lazy propagation postpones
updates to child nodes until their values are explicitly needed during future queries or updates.

Complexity Analysis:
- Space Complexity: O(N)
- Build Tree: O(N) time
- Range Update: O(log N) time
- Range Query: O(log N) time
"""

from typing import List


class SegmentTreeLazy:
    """
    Segment Tree with Lazy Propagation for Range Sum Queries & Range Addition Updates.

    >>> nums = [1, 2, 3, 4, 5]
    >>> st = SegmentTreeLazy(nums)
    >>> st.query_range(0, 4)
    15
    >>> st.query_range(1, 3)
    9
    >>> st.update_range(1, 3, 10)  # Add 10 to indices 1, 2, 3 -> [1, 12, 13, 14, 5]
    >>> st.query_range(1, 3)
    39
    >>> st.query_range(0, 4)
    45
    """

    def __init__(self, data: List[int]):
        """Initialize segment tree with input array."""
        self.n = len(data)
        self.tree = [0] * (4 * max(self.n, 1))
        self.lazy = [0] * (4 * max(self.n, 1))
        if self.n > 0:
            self._build(data, 0, 0, self.n - 1)

    def _build(self, data: List[int], node: int, start: int, end: int) -> None:
        if start == end:
            self.tree[node] = data[start]
            return
        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        self._build(data, left_child, start, mid)
        self._build(data, right_child, mid + 1, end)
        self.tree[node] = self.tree[left_child] + self.tree[right_child]

    def _push_lazy(self, node: int, start: int, end: int) -> None:
        """Push pending lazy updates to child nodes."""
        if self.lazy[node] != 0:
            val = self.lazy[node]
            self.tree[node] += (end - start + 1) * val
            if start != end:
                self.lazy[2 * node + 1] += val
                self.lazy[2 * node + 2] += val
            self.lazy[node] = 0

    def update_range(self, l: int, r: int, value: int) -> None:
        """
        Add `value` to all elements in index range [l, r] inclusive.
        Time Complexity: O(log N)
        """
        if self.n == 0 or l > r or l >= self.n or r < 0:
            return
        self._update_range(0, 0, self.n - 1, max(0, l), min(self.n - 1, r), value)

    def _update_range(
        self, node: int, start: int, end: int, l: int, r: int, value: int
    ) -> None:
        self._push_lazy(node, start, end)

        if start > end or start > r or end < l:
            return

        if l <= start and end <= r:
            self.tree[node] += (end - start + 1) * value
            if start != end:
                self.lazy[2 * node + 1] += value
                self.lazy[2 * node + 2] += value
            return

        mid = (start + end) // 2
        left_child = 2 * node + 1
        right_child = 2 * node + 2
        self._update_range(left_child, start, mid, l, r, value)
        self._update_range(right_child, mid + 1, end, l, r, value)
        self.tree[node] = self.tree[left_child] + self.tree[right_child]

    def query_range(self, l: int, r: int) -> int:
        """
        Compute sum of elements in index range [l, r] inclusive.
        Time Complexity: O(log N)
        """
        if self.n == 0 or l > r or l >= self.n or r < 0:
            return 0
        return self._query_range(0, 0, self.n - 1, max(0, l), min(self.n - 1, r))

    def _query_range(self, node: int, start: int, end: int, l: int, r: int) -> int:
        if start > end or start > r or end < l:
            return 0

        self._push_lazy(node, start, end)

        if l <= start and end <= r:
            return self.tree[node]

        mid = (start + end) // 2
        left_val = self._query_range(2 * node + 1, start, mid, l, r)
        right_val = self._query_range(2 * node + 2, mid + 1, end, l, r)
        return left_val + right_val


if __name__ == "__main__":
    import doctest

    results = doctest.testmod()
    if results.failed == 0:
        print(f"All {results.attempted} Lazy Segment Tree doctests passed successfully!")
