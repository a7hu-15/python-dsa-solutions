"""
Fenwick Tree (Binary Indexed Tree / BIT) Implementation in Python.

A Fenwick Tree or Binary Indexed Tree is a data structure that can efficiently
update elements and calculate prefix sums in a table of numbers.

Complexity Analysis:
- Space Complexity: O(N)
- Build Tree: O(N log N) or O(N)
- Point Update: O(log N)
- Prefix Sum Query: O(log N)
- Range Sum Query: O(log N)
"""

from typing import List


class FenwickTree:
    """
    1-indexed Fenwick Tree implementation supporting point updates and range sum queries.

    >>> nums = [1, 3, 5, 7, 9, 11]
    >>> ft = FenwickTree(nums)
    >>> ft.query(3)
    16
    >>> ft.range_query(1, 3)
    15
    >>> ft.update(1, 4)  # Add 4 to index 1 (making element 3 + 4 = 7)
    >>> ft.range_query(1, 3)
    19
    """

    def __init__(self, data: List[int]):
        """Initialize Fenwick Tree with array data."""
        self.n = len(data)
        self.tree = [0] * (self.n + 1)
        for i, val in enumerate(data):
            self.update(i, val)

    def update(self, index: int, delta: int) -> None:
        """
        Add delta to element at 0-indexed position 'index'.
        Time Complexity: O(log N)
        """
        if index < 0 or index >= self.n:
            raise IndexError("Index out of bounds")

        i = index + 1
        while i <= self.n:
            self.tree[i] += delta
            i += i & (-i)

    def query(self, index: int) -> int:
        """
        Compute prefix sum from 0 to 0-indexed position 'index'.
        Time Complexity: O(log N)
        """
        if index < 0:
            return 0
        if index >= self.n:
            index = self.n - 1

        prefix_sum = 0
        i = index + 1
        while i > 0:
            prefix_sum += self.tree[i]
            i -= i & (-i)
        return prefix_sum

    def range_query(self, left: int, right: int) -> int:
        """
        Compute sum of elements in range [left, right] inclusive.
        Time Complexity: O(log N)
        """
        if left > right or left >= self.n or right < 0:
            return 0
        return self.query(right) - self.query(left - 1)


if __name__ == "__main__":
    import doctest
    results = doctest.testmod()
    if results.failed == 0:
        print(f"All {results.attempted} Fenwick Tree doctests passed successfully!")
