"""
Disjoint Set Union (DSU / Union-Find) Implementation in Python.

Disjoint Set Union (Union-Find) is a data structure that keeps track of a set of elements partitioned
into a number of disjoint (non-overlapping) subsets. It supports two primary operations efficiently:
1. `find(x)`: Determine which subset a particular element `x` belongs to (with Path Compression).
2. `union(x, y)`: Join two subsets into a single subset (using Union by Rank/Size).

Complexity Analysis:
- Time Complexity: O(α(N)) per find/union operation, where α is the Inverse Ackermann function
  (effectively O(1) amortized in practice).
- Space Complexity: O(N) to store parent pointers and ranks/sizes.
"""

from typing import Dict, Generic, List, TypeVar, Union, Optional

T = TypeVar("T")


class DisjointSet(Generic[T]):
    """
    Disjoint Set Union (DSU) supporting path compression and union-by-rank.

    Supports both 0-indexed integer elements and arbitrary hashable elements.
    """

    def __init__(self, elements: Optional[List[T]] = None, size: Optional[int] = None):
        """
        Initialize DSU either with a specified integer size [0..size-1] or a list of initial elements.

        :param elements: Optional collection of initial elements.
        :param size: Optional count of integer elements from 0 to size-1.
        """
        self.parent: Dict[T, T] = {}
        self.rank: Dict[T, int] = {}
        self.size: Dict[T, int] = {}
        self._num_components: int = 0

        if size is not None:
            for i in range(size):
                self.add(i)  # type: ignore
        elif elements is not None:
            for elem in elements:
                self.add(elem)

    def add(self, x: T) -> bool:
        """
        Add a new element to the disjoint set as its own isolated set.

        :param x: Element to add.
        :return: True if newly added, False if already present.
        """
        if x in self.parent:
            return False
        self.parent[x] = x
        self.rank[x] = 0
        self.size[x] = 1
        self._num_components += 1
        return True

    def find(self, x: T) -> T:
        """
        Find the representative (root) of the set containing `x` with Path Compression.

        :param x: Element to query.
        :return: Representative element of the set.
        :raises KeyError: If `x` has not been added to the DSU.
        """
        if x not in self.parent:
            raise KeyError(f"Element '{x}' not found in DisjointSet.")

        # Path compression: make every visited node point directly to the root
        root = x
        while root != self.parent[root]:
            root = self.parent[root]

        curr = x
        while curr != root:
            nxt = self.parent[curr]
            self.parent[curr] = root
            curr = nxt

        return root

    def union(self, x: T, y: T) -> bool:
        """
        Unite the sets containing elements `x` and `y` using Union by Rank.

        :param x: First element.
        :param y: Second element.
        :return: True if two separate sets were merged, False if they were already in the same set.
        """
        root_x = self.find(x)
        root_y = self.find(y)

        if root_x == root_y:
            return False

        # Union by rank: attach smaller tree under root of higher rank tree
        if self.rank[root_x] < self.rank[root_y]:
            root_x, root_y = root_y, root_x

        self.parent[root_y] = root_x
        self.size[root_x] += self.size[root_y]

        if self.rank[root_x] == self.rank[root_y]:
            self.rank[root_x] += 1

        self._num_components -= 1
        return True

    def connected(self, x: T, y: T) -> bool:
        """
        Check whether elements `x` and `y` belong to the same subset.

        :param x: First element.
        :param y: Second element.
        :return: True if connected, False otherwise.
        """
        return self.find(x) == self.find(y)

    def get_set_size(self, x: T) -> int:
        """
        Return the total number of elements in the subset containing `x`.

        :param x: Target element.
        :return: Integer size of the set.
        """
        return self.size[self.find(x)]

    @property
    def num_components(self) -> int:
        """Return the total number of disjoint sets (connected components)."""
        return self._num_components


if __name__ == "__main__":
    import unittest

    class TestDisjointSet(unittest.TestCase):
        def test_basic_union_find(self):
            dsu = DisjointSet[int](size=5)
            self.assertEqual(dsu.num_components, 5)

            self.assertFalse(dsu.connected(0, 1))
            self.assertTrue(dsu.union(0, 1))
            self.assertTrue(dsu.connected(0, 1))
            self.assertEqual(dsu.num_components, 4)

            # Redundant union should return False
            self.assertFalse(dsu.union(0, 1))
            self.assertEqual(dsu.num_components, 4)

        def test_component_merging(self):
            dsu = DisjointSet[str](elements=["A", "B", "C", "D", "E"])
            dsu.union("A", "B")
            dsu.union("C", "D")
            self.assertEqual(dsu.num_components, 3)

            dsu.union("B", "C")
            self.assertTrue(dsu.connected("A", "D"))
            self.assertEqual(dsu.get_set_size("A"), 4)
            self.assertEqual(dsu.num_components, 2)

        def test_key_error(self):
            dsu = DisjointSet[int](size=3)
            with self.assertRaises(KeyError):
                dsu.find(10)

    unittest.main()
