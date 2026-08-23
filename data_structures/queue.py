"""
Queue and Double-Ended Queue (Deque) Data Structures

A Queue is a linear data structure that follows the FIFO (First In, First Out)
principle. The first element added is the first one to be removed.

A Deque (Double-Ended Queue) allows insertion and deletion from both ends
(front and rear) in O(1) time complexity.

Operations & Time Complexity (Queue):
    - Enqueue: O(1) — add element to rear
    - Dequeue: O(1) — remove element from front
    - Peek:    O(1) — view front element
    - isEmpty: O(1)

Operations & Time Complexity (Deque):
    - Append:      O(1) — add to right/rear
    - AppendLeft:  O(1) — add to left/front
    - Pop:         O(1) — remove from right/rear
    - PopLeft:     O(1) — remove from left/front
    - PeekFront:   O(1) — view front
    - PeekRear:    O(1) — view rear

Space Complexity: O(n)

>>> q = Queue()
>>> q.is_empty()
True
>>> q.enqueue(1)
>>> q.enqueue(2)
>>> q.enqueue(3)
>>> str(q)
'Queue([1, 2, 3])'
>>> q.peek()
1
>>> q.dequeue()
1
>>> len(q)
2
"""

from __future__ import annotations

from collections import deque
from typing import Any, Generic, Iterator, TypeVar

T = TypeVar("T")


class Queue(Generic[T]):
    """
    First-In-First-Out (FIFO) Queue implementation.

    >>> q = Queue()
    >>> q.enqueue("Apple")
    >>> q.enqueue("Banana")
    >>> q.enqueue("Cherry")
    >>> len(q)
    3
    >>> q.peek()
    'Apple'
    >>> q.dequeue()
    'Apple'
    >>> q.dequeue()
    'Banana'
    >>> q.is_empty()
    False
    >>> q.dequeue()
    'Cherry'
    >>> q.is_empty()
    True
    """

    def __init__(self, max_size: int | None = None) -> None:
        """
        Initialize an empty Queue.

        Args:
            max_size: Optional maximum capacity. None means unlimited capacity.
        """
        self._items: deque[T] = deque()
        self._max_size = max_size

    def is_empty(self) -> bool:
        """Return True if the queue contains no elements."""
        return len(self._items) == 0

    def is_full(self) -> bool:
        """Return True if the queue has reached its maximum size."""
        if self._max_size is None:
            return False
        return len(self._items) >= self._max_size

    def enqueue(self, item: T) -> None:
        """
        Add an item to the rear of the queue.

        Raises:
            OverflowError: If the queue is full.
        """
        if self.is_full():
            raise OverflowError(f"Cannot enqueue to full queue (max_size={self._max_size})")
        self._items.append(item)

    def dequeue(self) -> T:
        """
        Remove and return the item at the front of the queue.

        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot dequeue from an empty queue")
        return self._items.popleft()

    def peek(self) -> T:
        """
        Return the item at the front of the queue without removing it.

        Raises:
            IndexError: If the queue is empty.
        """
        if self.is_empty():
            raise IndexError("Cannot peek into an empty queue")
        return self._items[0]

    def clear(self) -> None:
        """Remove all items from the queue."""
        self._items.clear()

    def __len__(self) -> int:
        return len(self._items)

    def __str__(self) -> str:
        return f"Queue({list(self._items)})"

    def __repr__(self) -> str:
        return f"Queue(items={list(self._items)}, max_size={self._max_size})"

    def __contains__(self, item: T) -> bool:
        return item in self._items

    def __iter__(self) -> Iterator[T]:
        return iter(self._items)


class Deque(Generic[T]):
    """
    Double-Ended Queue (Deque) implementation allowing O(1) operations at both ends.

    >>> d = Deque()
    >>> d.append_rear(10)
    >>> d.append_front(5)
    >>> d.append_rear(20)
    >>> str(d)
    'Deque([5, 10, 20])'
    >>> d.pop_front()
    5
    >>> d.pop_rear()
    20
    >>> d.peek_front()
    10
    """

    def __init__(self, max_size: int | None = None) -> None:
        """Initialize an empty Deque."""
        self._items: deque[T] = deque()
        self._max_size = max_size

    def is_empty(self) -> bool:
        """Return True if the deque contains no elements."""
        return len(self._items) == 0

    def is_full(self) -> bool:
        """Return True if the deque has reached maximum capacity."""
        if self._max_size is None:
            return False
        return len(self._items) >= self._max_size

    def append_front(self, item: T) -> None:
        """Add an item to the front of the deque."""
        if self.is_full():
            raise OverflowError(f"Deque is full (max_size={self._max_size})")
        self._items.appendleft(item)

    def append_rear(self, item: T) -> None:
        """Add an item to the rear of the deque."""
        if self.is_full():
            raise OverflowError(f"Deque is full (max_size={self._max_size})")
        self._items.append(item)

    def pop_front(self) -> T:
        """Remove and return item from the front of the deque."""
        if self.is_empty():
            raise IndexError("Cannot pop from front of an empty deque")
        return self._items.popleft()

    def pop_rear(self) -> T:
        """Remove and return item from the rear of the deque."""
        if self.is_empty():
            raise IndexError("Cannot pop from rear of an empty deque")
        return self._items.pop()

    def peek_front(self) -> T:
        """View item at the front of the deque."""
        if self.is_empty():
            raise IndexError("Cannot peek front of an empty deque")
        return self._items[0]

    def peek_rear(self) -> T:
        """View item at the rear of the deque."""
        if self.is_empty():
            raise IndexError("Cannot peek rear of an empty deque")
        return self._items[-1]

    def __len__(self) -> int:
        return len(self._items)

    def __str__(self) -> str:
        return f"Deque({list(self._items)})"

    def __repr__(self) -> str:
        return f"Deque(items={list(self._items)}, max_size={self._max_size})"

    def __iter__(self) -> Iterator[T]:
        return iter(self._items)


if __name__ == "__main__":
    import doctest

    print("Running Queue & Deque doctests...")
    results = doctest.testmod()
    if results.failed == 0:
        print(f"✅ All {results.attempted} tests passed!")
    else:
        print(f"❌ {results.failed} tests failed out of {results.attempted}")
