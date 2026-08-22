"""
Singly Linked List Data Structure

A linked list is a linear data structure where each element (node) contains
a value and a reference (pointer) to the next node in the sequence.

Operations & Time Complexity:
    - Access:    O(n)
    - Search:    O(n)
    - Insert at head: O(1)
    - Insert at tail: O(n) — O(1) with tail pointer
    - Delete:    O(n)

Space Complexity: O(n)

>>> ll = LinkedList()
>>> ll.is_empty()
True

>>> ll.push_front(3)
>>> ll.push_front(2)
>>> ll.push_front(1)
>>> str(ll)
'1 -> 2 -> 3 -> None'

>>> len(ll)
3

>>> ll.push_back(4)
>>> str(ll)
'1 -> 2 -> 3 -> 4 -> None'

>>> ll.pop_front()
1
>>> str(ll)
'2 -> 3 -> 4 -> None'

>>> ll.find(3)
True

>>> ll.find(99)
False

>>> ll.delete(3)
True
>>> str(ll)
'2 -> 4 -> None'
"""

from __future__ import annotations

from typing import Any


class Node:
    """A node in a singly linked list."""

    __slots__ = ("data", "next_node")

    def __init__(self, data: Any, next_node: Node | None = None) -> None:
        self.data = data
        self.next_node = next_node

    def __repr__(self) -> str:
        return f"Node({self.data})"


class LinkedList:
    """
    Singly Linked List implementation.

    Supports common operations: push, pop, find, delete, reverse, and more.

    >>> ll = LinkedList.from_list([1, 2, 3, 4, 5])
    >>> str(ll)
    '1 -> 2 -> 3 -> 4 -> 5 -> None'

    >>> ll.reverse()
    >>> str(ll)
    '5 -> 4 -> 3 -> 2 -> 1 -> None'
    """

    def __init__(self) -> None:
        self.head: Node | None = None
        self._size: int = 0

    def __len__(self) -> int:
        return self._size

    def __str__(self) -> str:
        parts = []
        current = self.head
        while current is not None:
            parts.append(str(current.data))
            current = current.next_node
        parts.append("None")
        return " -> ".join(parts)

    def __iter__(self):
        """
        Iterate over the linked list values.

        >>> ll = LinkedList.from_list([1, 2, 3])
        >>> list(ll)
        [1, 2, 3]
        """
        current = self.head
        while current is not None:
            yield current.data
            current = current.next_node

    def __contains__(self, value: Any) -> bool:
        """
        Check if a value exists in the list.

        >>> ll = LinkedList.from_list([1, 2, 3])
        >>> 2 in ll
        True
        >>> 5 in ll
        False
        """
        return self.find(value)

    def is_empty(self) -> bool:
        """Return True if the list is empty."""
        return self.head is None

    def push_front(self, data: Any) -> None:
        """
        Insert a new node at the beginning of the list. O(1).

        Args:
            data: The value to insert.

        >>> ll = LinkedList()
        >>> ll.push_front(1)
        >>> ll.push_front(2)
        >>> str(ll)
        '2 -> 1 -> None'
        """
        new_node = Node(data, self.head)
        self.head = new_node
        self._size += 1

    def push_back(self, data: Any) -> None:
        """
        Insert a new node at the end of the list. O(n).

        Args:
            data: The value to insert.

        >>> ll = LinkedList()
        >>> ll.push_back(1)
        >>> ll.push_back(2)
        >>> str(ll)
        '1 -> 2 -> None'
        """
        new_node = Node(data)

        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next_node is not None:
                current = current.next_node
            current.next_node = new_node

        self._size += 1

    def pop_front(self) -> Any:
        """
        Remove and return the first element. O(1).

        Returns:
            The data of the removed node.

        Raises:
            IndexError: If the list is empty.

        >>> ll = LinkedList.from_list([10, 20, 30])
        >>> ll.pop_front()
        10
        >>> str(ll)
        '20 -> 30 -> None'
        """
        if self.head is None:
            raise IndexError("pop from empty linked list")

        data = self.head.data
        self.head = self.head.next_node
        self._size -= 1
        return data

    def find(self, value: Any) -> bool:
        """
        Check if a value exists in the list. O(n).

        Args:
            value: The value to search for.

        Returns:
            True if found, False otherwise.

        >>> ll = LinkedList.from_list([1, 2, 3])
        >>> ll.find(2)
        True
        >>> ll.find(5)
        False
        """
        current = self.head
        while current is not None:
            if current.data == value:
                return True
            current = current.next_node
        return False

    def delete(self, value: Any) -> bool:
        """
        Delete the first occurrence of a value. O(n).

        Args:
            value: The value to delete.

        Returns:
            True if the value was found and deleted, False otherwise.

        >>> ll = LinkedList.from_list([1, 2, 3, 2])
        >>> ll.delete(2)
        True
        >>> str(ll)
        '1 -> 3 -> 2 -> None'
        >>> ll.delete(99)
        False
        """
        if self.head is None:
            return False

        if self.head.data == value:
            self.head = self.head.next_node
            self._size -= 1
            return True

        current = self.head
        while current.next_node is not None:
            if current.next_node.data == value:
                current.next_node = current.next_node.next_node
                self._size -= 1
                return True
            current = current.next_node

        return False

    def reverse(self) -> None:
        """
        Reverse the linked list in-place. O(n).

        >>> ll = LinkedList.from_list([1, 2, 3, 4])
        >>> ll.reverse()
        >>> str(ll)
        '4 -> 3 -> 2 -> 1 -> None'
        """
        prev = None
        current = self.head

        while current is not None:
            next_node = current.next_node
            current.next_node = prev
            prev = current
            current = next_node

        self.head = prev

    def to_list(self) -> list:
        """
        Convert the linked list to a Python list.

        >>> ll = LinkedList.from_list([1, 2, 3])
        >>> ll.to_list()
        [1, 2, 3]
        """
        return list(self)

    @classmethod
    def from_list(cls, values: list) -> LinkedList:
        """
        Create a LinkedList from a Python list.

        Args:
            values: A list of values.

        Returns:
            A new LinkedList containing the values.

        >>> ll = LinkedList.from_list([10, 20, 30])
        >>> str(ll)
        '10 -> 20 -> 30 -> None'
        """
        ll = cls()
        for value in values:
            ll.push_back(value)
        return ll


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # Demo
    ll = LinkedList()
    for val in [10, 20, 30, 40, 50]:
        ll.push_back(val)

    print(f"List:     {ll}")
    print(f"Length:   {len(ll)}")
    print(f"Find 30: {ll.find(30)}")

    ll.reverse()
    print(f"Reversed: {ll}")

    ll.delete(30)
    print(f"Delete 30: {ll}")
