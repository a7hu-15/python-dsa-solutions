"""
Skip List Data Structure Implementation in Python.

A Skip List is a probabilistic data structure that allows O(log n) search, insertion,
and deletion operations within an ordered sequence of elements. It maintains multiple layers
of linked lists, where higher layers act as express lanes to skip elements.

Complexity Analysis:
- Time Complexity:
  - Search: O(log n) average, O(n) worst-case
  - Insertion: O(log n) average, O(n) worst-case
  - Deletion: O(log n) average, O(n) worst-case
- Space Complexity: O(n) average
"""

import random
from typing import Any, List, Optional, Tuple


class SkipNode:
    """Node structure for Skip List."""

    def __init__(self, key: Any, value: Any = None, level: int = 1):
        self.key = key
        self.value = value if value is not None else key
        # forward array stores pointers to next nodes at each level (0 to level-1)
        self.forward: List[Optional["SkipNode"]] = [None] * level

    @property
    def level(self) -> int:
        return len(self.forward)


class SkipList:
    """
    Skip List probabilistic ordered map / set implementation.

    >>> sl = SkipList(max_level=4, p=0.5)
    >>> sl.insert(3, "three")
    >>> sl.insert(6, "six")
    >>> sl.insert(7, "seven")
    >>> sl.search(6)
    'six'
    >>> sl.search(10) is None
    True
    >>> sl.delete(6)
    True
    >>> sl.search(6) is None
    True
    """

    def __init__(self, max_level: int = 16, p: float = 0.5):
        """
        Initialize Skip List with maximum level and probability p.

        :param max_level: Maximum number of height levels permitted.
        :param p: Probability factor for node level generation (typically 0.5 or 0.25).
        """
        if max_level <= 0:
            raise ValueError("max_level must be greater than 0")
        if not (0.0 < p < 1.0):
            raise ValueError("Probability p must be between 0.0 and 1.0")

        self.max_level = max_level
        self.p = p
        self.header = SkipNode(key=float("-inf"), level=self.max_level)
        self.current_level = 1
        self._size = 0

    def _random_level(self) -> int:
        """Generate a random level for a new node using geometric distribution."""
        lvl = 1
        while random.random() < self.p and lvl < self.max_level:
            lvl += 1
        return lvl

    def search(self, key: Any) -> Optional[Any]:
        """
        Search for a key in the Skip List.

        :param key: Target key to search for.
        :return: Value associated with key if present, otherwise None.
        """
        current = self.header
        # Traverse top-down from current highest level
        for i in range(self.current_level - 1, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]

        current = current.forward[0]
        if current and current.key == key:
            return current.value
        return None

    def insert(self, key: Any, value: Any = None) -> None:
        """
        Insert a key-value pair into the Skip List or update value if key exists.

        :param key: Key to insert.
        :param value: Associated value (defaults to key).
        """
        if value is None:
            value = key

        update = [None] * self.max_level
        current = self.header

        for i in range(self.current_level - 1, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        # Key already exists: update value
        if current and current.key == key:
            current.value = value
            return

        # Key does not exist: generate random level for new node
        new_level = self._random_level()

        if new_level > self.current_level:
            for i in range(self.current_level, new_level):
                update[i] = self.header
            self.current_level = new_level

        new_node = SkipNode(key=key, value=value, level=new_level)
        for i in range(new_level):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

        self._size += 1

    def delete(self, key: Any) -> bool:
        """
        Remove a key from the Skip List.

        :param key: Key to delete.
        :return: True if key was found and removed, False otherwise.
        """
        update = [None] * self.max_level
        current = self.header

        for i in range(self.current_level - 1, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current and current.key == key:
            for i in range(self.current_level):
                if update[i].forward[i] != current:
                    break
                update[i].forward[i] = current.forward[i]

            # Decrease current level if top levels are empty
            while self.current_level > 1 and self.header.forward[self.current_level - 1] is None:
                self.current_level -= 1

            self._size -= 1
            return True

        return False

    def to_list(self) -> List[Tuple[Any, Any]]:
        """Return all (key, value) pairs in ascending key order."""
        result = []
        current = self.header.forward[0]
        while current:
            result.append((current.key, current.value))
            current = current.forward[0]
        return result

    def __len__(self) -> int:
        return self._size

    def __contains__(self, key: Any) -> bool:
        return self.search(key) is not None

    def display(self) -> str:
        """Return string visualization of skip list levels."""
        lines = []
        for lvl in range(self.current_level - 1, -1, -1):
            line = f"Level {lvl + 1}: "
            node = self.header.forward[lvl]
            nodes = []
            while node:
                nodes.append(f"[{node.key}]")
                node = node.forward[lvl]
            line += " -> ".join(nodes) if nodes else "Empty"
            lines.append(line)
        return "\n".join(lines)


if __name__ == "__main__":
    import unittest

    class TestSkipList(unittest.TestCase):
        def test_insert_and_search(self):
            sl = SkipList(max_level=4, p=0.5)
            keys = [10, 20, 5, 15, 30]
            for k in keys:
                sl.insert(k, f"val_{k}")

            self.assertEqual(len(sl), 5)
            for k in keys:
                self.assertEqual(sl.search(k), f"val_{k}")

            self.assertIsNone(sl.search(99))

        def test_update_existing_key(self):
            sl = SkipList()
            sl.insert(5, "old")
            self.assertEqual(sl.search(5), "old")
            sl.insert(5, "new")
            self.assertEqual(sl.search(5), "new")
            self.assertEqual(len(sl), 1)

        def test_delete(self):
            sl = SkipList()
            sl.insert(1, "one")
            sl.insert(2, "two")
            sl.insert(3, "three")

            self.assertTrue(sl.delete(2))
            self.assertEqual(len(sl), 2)
            self.assertIsNone(sl.search(2))
            self.assertFalse(sl.delete(2))
            self.assertFalse(sl.delete(99))

        def test_sorted_order(self):
            sl = SkipList()
            items = [50, 10, 40, 20, 30]
            for item in items:
                sl.insert(item)
            self.assertEqual([k for k, _ in sl.to_list()], [10, 20, 30, 40, 50])

    unittest.main()
