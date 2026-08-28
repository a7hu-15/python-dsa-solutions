"""
Least Recently Used (LRU) Cache Implementation in Python.

An LRU Cache organizes items in order of use, allowing you to quickly identify
which item hasn't been used for the longest amount of time. It achieves O(1) time
complexity for both `get` and `put` operations by combining a Hash Map with a Doubly Linked List.

Complexity Analysis:
- Time Complexity: O(1) for get(key) and put(key, value)
- Space Complexity: O(capacity)
"""

from typing import Any, Dict, Optional


class Node:
    """Doubly Linked List node for LRU Cache."""

    def __init__(self, key: Any = None, value: Any = None):
        self.key = key
        self.value = value
        self.prev: Optional['Node'] = None
        self.next: Optional['Node'] = None


class LRUCache:
    """
    LRU Cache implementation with fixed capacity.

    >>> cache = LRUCache(2)
    >>> cache.put(1, 10)
    >>> cache.put(2, 20)
    >>> cache.get(1)
    10
    >>> cache.put(3, 30)  # Evicts key 2
    >>> cache.get(2)
    -1
    >>> cache.put(4, 40)  # Evicts key 1
    >>> cache.get(1)
    -1
    >>> cache.get(3)
    30
    >>> cache.get(4)
    40
    """

    def __init__(self, capacity: int):
        if capacity <= 0:
            raise ValueError("Capacity must be positive")
        self.capacity = capacity
        self.cache: Dict[Any, Node] = {}

        # Sentinel dummy nodes
        self.head = Node()
        self.tail = Node()
        self.head.next = self.tail
        self.tail.prev = self.head

    def _add_node(self, node: Node) -> None:
        """Always add the new node right after head."""
        node.prev = self.head
        node.next = self.head.next

        self.head.next.prev = node
        self.head.next = node

    def _remove_node(self, node: Node) -> None:
        """Remove an existing node from the doubly linked list."""
        prev = node.prev
        nxt = node.next

        prev.next = nxt
        nxt.prev = prev

    def _move_to_head(self, node: Node) -> None:
        """Move node to the front (most recently used)."""
        self._remove_node(node)
        self._add_node(node)

    def _pop_tail(self) -> Node:
        """Pop the current least recently used item."""
        res = self.tail.prev
        self._remove_node(res)
        return res

    def get(self, key: Any) -> Any:
        """Get value for key if present, else return -1. O(1) time."""
        node = self.cache.get(key)
        if not node:
            return -1

        self._move_to_head(node)
        return node.value

    def put(self, key: Any, value: Any) -> None:
        """Put key-value pair in cache. Evict LRU item if capacity is exceeded. O(1) time."""
        node = self.cache.get(key)

        if not node:
            newNode = Node(key, value)
            self.cache[key] = newNode
            self._add_node(newNode)

            if len(self.cache) > self.capacity:
                tail = self._pop_tail()
                del self.cache[tail.key]
        else:
            node.value = value
            self._move_to_head(node)


if __name__ == "__main__":
    import doctest
    results = doctest.testmod()
    if results.failed == 0:
        print(f"All {results.attempted} LRU Cache doctests passed successfully!")
