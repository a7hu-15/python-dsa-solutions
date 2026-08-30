"""
B-Tree Self-Balancing Multi-way Search Tree Implementation in Python.

A B-Tree is a self-balancing tree data structure that maintains sorted data and allows
searches, sequential access, insertions, and deletions in logarithmic time. Unlike binary search trees,
a B-Tree node can have more than two children and multiple keys.

Key Properties (Degree t >= 2):
1. Every node has at most 2t - 1 keys.
2. Every internal node (except root) has at least t - 1 keys and at least t children.
3. The root has at least 1 key if non-empty.
4. All leaves appear on the same level.

Complexity Analysis:
- Time Complexity:
  - Search: O(t * log_t n)
  - Insertion: O(t * log_t n)
  - Deletion: O(t * log_t n)
- Space Complexity: O(n)
"""

from typing import Any, List, Optional, Tuple


class BTreeNode:
    """Node in a B-Tree."""

    def __init__(self, leaf: bool = True):
        self.leaf: bool = leaf
        self.keys: List[Any] = []
        self.children: List["BTreeNode"] = []

    def is_full(self, t: int) -> bool:
        """Check if node contains maximum permitted keys (2t - 1)."""
        return len(self.keys) == 2 * t - 1


class BTree:
    """
    B-Tree implementation with minimum degree t.

    >>> btree = BTree(t=2)
    >>> for key in [10, 20, 5, 6, 12, 30, 7, 17]:
    ...     btree.insert(key)
    >>> btree.search(6) is not None
    True
    >>> btree.search(99) is None
    True
    >>> btree.inorder()
    [5, 6, 7, 10, 12, 17, 20, 30]
    """

    def __init__(self, t: int = 3):
        """
        Initialize B-Tree.

        :param t: Minimum degree (t >= 2). A node has at most 2t-1 keys and 2t children.
        """
        if t < 2:
            raise ValueError("B-Tree minimum degree t must be at least 2.")
        self.t: int = t
        self.root: BTreeNode = BTreeNode(leaf=True)

    def search(self, key: Any, node: Optional[BTreeNode] = None) -> Optional[Tuple[BTreeNode, int]]:
        """
        Search for a key starting from given node or root.

        :param key: Target key to search for.
        :param node: Node to start search from (defaults to root).
        :return: Tuple (node, key_index) if key is found, otherwise None.
        """
        if node is None:
            node = self.root

        i = 0
        while i < len(node.keys) and key > node.keys[i]:
            i += 1

        if i < len(node.keys) and key == node.keys[i]:
            return node, i

        if node.leaf:
            return None

        return self.search(key, node.children[i])

    def insert(self, key: Any) -> None:
        """
        Insert a key into the B-Tree. Splits full nodes proactively on downward path.

        :param key: Key to insert.
        """
        root = self.root

        if root.is_full(self.t):
            # Create a new root and split old root
            new_root = BTreeNode(leaf=False)
            new_root.children.append(self.root)
            self._split_child(new_root, 0)
            self.root = new_root
            self._insert_non_full(self.root, key)
        else:
            self._insert_non_full(root, key)

    def _split_child(self, parent: BTreeNode, i: int) -> None:
        """
        Split the i-th full child of parent.

        :param parent: Parent node whose child is being split.
        :param i: Index of child in parent.children.
        """
        t = self.t
        y = parent.children[i]
        z = BTreeNode(leaf=y.leaf)

        # Median key moves up to parent
        median_key = y.keys[t - 1]

        # Right half of keys go to z
        z.keys = y.keys[t:]
        y.keys = y.keys[: t - 1]

        # Right half of children go to z if y is not a leaf
        if not y.leaf:
            z.children = y.children[t:]
            y.children = y.children[:t]

        # Insert z into parent's children and median_key into parent's keys
        parent.children.insert(i + 1, z)
        parent.keys.insert(i, median_key)

    def _insert_non_full(self, node: BTreeNode, key: Any) -> None:
        """Insert key into a node known to be non-full."""
        i = len(node.keys) - 1

        if node.leaf:
            node.keys.append(None)
            while i >= 0 and key < node.keys[i]:
                node.keys[i + 1] = node.keys[i]
                i -= 1
            node.keys[i + 1] = key
        else:
            while i >= 0 and key < node.keys[i]:
                i -= 1
            i += 1

            if node.children[i].is_full(self.t):
                self._split_child(node, i)
                if key > node.keys[i]:
                    i += 1

            self._insert_non_full(node.children[i], key)

    def inorder(self, node: Optional[BTreeNode] = None) -> List[Any]:
        """Return in-order sorted list of all keys in the B-Tree."""
        if node is None:
            node = self.root

        result = []
        if node.leaf:
            return list(node.keys)

        for i in range(len(node.keys)):
            result.extend(self.inorder(node.children[i]))
            result.append(node.keys[i])

        if node.children:
            result.extend(self.inorder(node.children[-1]))

        return result


if __name__ == "__main__":
    import unittest

    class TestBTree(unittest.TestCase):
        def test_insertion_and_search(self):
            btree = BTree(t=3)
            values = [10, 20, 5, 6, 12, 30, 7, 17, 3, 22, 24, 27, 45, 33]
            for v in values:
                btree.insert(v)

            for v in values:
                self.assertIsNotNone(btree.search(v))

            self.assertIsNone(btree.search(100))
            self.assertIsNone(btree.search(0))

        def test_inorder_traversal(self):
            btree = BTree(t=2)
            values = [50, 10, 40, 20, 30, 5, 60, 25, 35]
            for v in values:
                btree.insert(v)

            sorted_values = sorted(values)
            self.assertEqual(btree.inorder(), sorted_values)

        def test_small_degree_b_tree(self):
            btree = BTree(t=2)  # 2-3-4 tree structure
            for i in range(1, 20):
                btree.insert(i)
            self.assertEqual(btree.inorder(), list(range(1, 20)))

    unittest.main()
