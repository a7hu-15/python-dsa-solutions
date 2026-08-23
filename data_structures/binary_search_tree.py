"""
Binary Search Tree (BST) Data Structure

A Binary Search Tree is a node-based binary tree data structure which has the
following properties:
    - The left subtree of a node contains only nodes with keys lesser than the node's key.
    - The right subtree of a node contains only nodes with keys greater than the node's key.
    - The left and right subtree each must also be a binary search tree.

Operations & Time Complexity:
    - Search:  Average O(log n), Worst O(n)
    - Insert:  Average O(log n), Worst O(n)
    - Delete:  Average O(log n), Worst O(n)
    - Minimum/Maximum: Average O(log n), Worst O(n)

Space Complexity: O(n) for tree storage, O(h) recursion stack depth (h = height).

>>> bst = BinarySearchTree()
>>> for val in [50, 30, 70, 20, 40, 60, 80]:
...     bst.insert(val)
>>> bst.inorder()
[20, 30, 40, 50, 60, 70, 80]
>>> bst.search(40)
True
>>> bst.search(100)
False
>>> bst.delete(30)
True
>>> bst.inorder()
[20, 40, 50, 60, 70, 80]
"""

from __future__ import annotations

from collections import deque
from typing import Any, Generic, TypeVar

T = TypeVar("T")


class TreeNode(Generic[T]):
    """Represents a node in a Binary Search Tree."""

    def __init__(self, val: T) -> None:
        self.val: T = val
        self.left: TreeNode[T] | None = None
        self.right: TreeNode[T] | None = None

    def __repr__(self) -> str:
        return f"TreeNode({self.val})"


class BinarySearchTree(Generic[T]):
    """
    Binary Search Tree implementation supporting insertion, deletion, searching,
    traversals (In-order, Pre-order, Post-order, Level-order), and tree properties.

    >>> bst = BinarySearchTree()
    >>> bst.is_empty()
    True
    >>> bst.insert(15)
    >>> bst.insert(10)
    >>> bst.insert(20)
    >>> bst.insert(8)
    >>> bst.insert(12)
    >>> bst.height()
    3
    >>> bst.min_val()
    8
    >>> bst.max_val()
    20
    >>> bst.preorder()
    [15, 10, 8, 12, 20]
    >>> bst.postorder()
    [8, 12, 10, 20, 15]
    >>> bst.level_order()
    [15, 10, 20, 8, 12]
    >>> bst.is_valid_bst()
    True
    """

    def __init__(self) -> None:
        """Initialize an empty Binary Search Tree."""
        self.root: TreeNode[T] | None = None
        self._size: int = 0

    def is_empty(self) -> bool:
        """Return True if the BST is empty."""
        return self.root is None

    def __len__(self) -> int:
        """Return total number of nodes in the BST."""
        return self._size

    def insert(self, val: T) -> None:
        """
        Insert a value into the BST. Duplicates are ignored.

        Args:
            val: Value to insert.
        """
        if self.root is None:
            self.root = TreeNode(val)
            self._size += 1
            return

        curr = self.root
        while True:
            if val == curr.val:
                # Value already exists
                return
            elif val < curr.val:
                if curr.left is None:
                    curr.left = TreeNode(val)
                    self._size += 1
                    return
                curr = curr.left
            else:
                if curr.right is None:
                    curr.right = TreeNode(val)
                    self._size += 1
                    return
                curr = curr.right

    def search(self, val: T) -> bool:
        """
        Search for a value in the BST.

        Returns:
            True if value exists in tree, False otherwise.
        """
        curr = self.root
        while curr is not None:
            if val == curr.val:
                return True
            elif val < curr.val:
                curr = curr.left
            else:
                curr = curr.right
        return False

    def min_val(self) -> T | None:
        """Return the minimum value in the BST."""
        if self.root is None:
            return None
        curr = self.root
        while curr.left is not None:
            curr = curr.left
        return curr.val

    def max_val(self) -> T | None:
        """Return the maximum value in the BST."""
        if self.root is None:
            return None
        curr = self.root
        while curr.right is not None:
            curr = curr.right
        return curr.val

    def delete(self, val: T) -> bool:
        """
        Delete a value from the BST if present.

        Returns:
            True if deletion was successful, False if value was not found.
        """
        initial_size = self._size
        self.root = self._delete_node(self.root, val)
        return self._size < initial_size

    def _delete_node(self, node: TreeNode[T] | None, val: T) -> TreeNode[T] | None:
        if node is None:
            return None

        if val < node.val:
            node.left = self._delete_node(node.left, val)
        elif val > node.val:
            node.right = self._delete_node(node.right, val)
        else:
            # Node found
            self._size -= 1

            # Case 1 & 2: Leaf node or single child
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Case 3: Two children
            # Find in-order successor (smallest node in right subtree)
            successor = node.right
            while successor.left is not None:
                successor = successor.left

            # Copy successor value and delete successor node
            node.val = successor.val
            # Increment size artificially because recursive call will decrement it
            self._size += 1
            node.right = self._delete_node(node.right, successor.val)

        return node

    def inorder(self) -> list[T]:
        """Return list of values in in-order traversal (sorted)."""
        result: list[T] = []

        def _traverse(node: TreeNode[T] | None) -> None:
            if node is not None:
                _traverse(node.left)
                result.append(node.val)
                _traverse(node.right)

        _traverse(self.root)
        return result

    def preorder(self) -> list[T]:
        """Return list of values in pre-order traversal (Root -> Left -> Right)."""
        result: list[T] = []

        def _traverse(node: TreeNode[T] | None) -> None:
            if node is not None:
                result.append(node.val)
                _traverse(node.left)
                _traverse(node.right)

        _traverse(self.root)
        return result

    def postorder(self) -> list[T]:
        """Return list of values in post-order traversal (Left -> Right -> Root)."""
        result: list[T] = []

        def _traverse(node: TreeNode[T] | None) -> None:
            if node is not None:
                _traverse(node.left)
                _traverse(node.right)
                result.append(node.val)

        _traverse(self.root)
        return result

    def level_order(self) -> list[T]:
        """Return list of values in level-order traversal (Breadth-First Search)."""
        if self.root is None:
            return []

        result: list[T] = []
        q: deque[TreeNode[T]] = deque([self.root])

        while q:
            curr = q.popleft()
            result.append(curr.val)
            if curr.left:
                q.append(curr.left)
            if curr.right:
                q.append(curr.right)

        return result

    def height(self) -> int:
        """Return height of the BST (number of nodes along longest root-to-leaf path)."""
        def _get_height(node: TreeNode[T] | None) -> int:
            if node is None:
                return 0
            return 1 + max(_get_height(node.left), _get_height(node.right))

        return _get_height(self.root)

    def is_valid_bst(self) -> bool:
        """
        Validate whether tree satisfies BST property.

        Returns:
            True if tree is a valid BST, False otherwise.
        """
        def _validate(node: TreeNode[T] | None, min_bound: Any, max_bound: Any) -> bool:
            if node is None:
                return True
            if (min_bound is not None and node.val <= min_bound) or \
               (max_bound is not None and node.val >= max_bound):
                return False
            return _validate(node.left, min_bound, node.val) and _validate(node.right, node.val, max_bound)

        return _validate(self.root, None, None)


if __name__ == "__main__":
    import doctest

    print("Running Binary Search Tree doctests...")
    results = doctest.testmod()
    if results.failed == 0:
        print(f"✅ All {results.attempted} tests passed!")
    else:
        print(f"❌ {results.failed} tests failed out of {results.attempted}")
