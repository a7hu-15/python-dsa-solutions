"""
Heap Sort Algorithm and Binary Heap Data Structure

Heap Sort is a comparison-based sorting algorithm that uses a Binary Heap data
structure. It builds a Max-Heap from the array and repeatedly extracts the maximum
element to place it at the end of the array.

Time Complexity:
    - Best Case:    O(n log n)
    - Average Case: O(n log n)
    - Worst Case:   O(n log n)

Space Complexity:
    - O(1) auxiliary space (in-place sorting)

>>> heap_sort([12, 11, 13, 5, 6, 7])
[5, 6, 7, 11, 12, 13]
>>> heap_sort([4, 10, 3, 5, 1], reverse=True)
[10, 5, 4, 3, 1]
>>> heap_sort([])
[]
>>> heap_sort([42])
[42]
"""

from __future__ import annotations

from typing import Any, Generic, TypeVar

T = TypeVar("T")


def _sift_down(arr: list[Any], n: int, i: int, reverse: bool = False) -> None:
    """
    Helper function to maintain the heap property for a subtree rooted at index i.

    Args:
        arr: Target list.
        n: Size of heap boundary.
        i: Subtree root index.
        reverse: If True, maintains Min-Heap property (for descending sort).
                 If False, maintains Max-Heap property (for ascending sort).
    """
    target_idx = i
    left = 2 * i + 1
    right = 2 * i + 2

    if reverse:
        # Min-Heap logic for descending sort
        if left < n and arr[left] < arr[target_idx]:
            target_idx = left
        if right < n and arr[right] < arr[target_idx]:
            target_idx = right
    else:
        # Max-Heap logic for ascending sort
        if left < n and arr[left] > arr[target_idx]:
            target_idx = left
        if right < n and arr[right] > arr[target_idx]:
            target_idx = right

    if target_idx != i:
        arr[i], arr[target_idx] = arr[target_idx], arr[i]
        _sift_down(arr, n, target_idx, reverse=reverse)


def heapify(arr: list[Any], reverse: bool = False) -> None:
    """
    Transform a list into a binary heap in O(n) time in-place.

    Args:
        arr: Mutable list to heapify.
        reverse: If True, builds a Min-Heap. If False, builds a Max-Heap.

    >>> nums = [3, 9, 2, 1, 4, 5]
    >>> heapify(nums)
    >>> nums[0]  # Root of Max-Heap is the maximum element
    9
    """
    n = len(arr)
    # Start from the last non-leaf node and sift down each node
    for i in range(n // 2 - 1, -1, -1):
        _sift_down(arr, n, i, reverse=reverse)


def heap_sort(arr: list[T], reverse: bool = False) -> list[T]:
    """
    Sort a list using Heap Sort. Returns a new sorted list (does not mutate original).

    Args:
        arr: Iterable of comparable elements.
        reverse: If True, sort in descending order. Otherwise ascending.

    Returns:
        New sorted list.

    >>> heap_sort([3, 1, 4, 1, 5, 9, 2, 6, 5])
    [1, 1, 2, 3, 4, 5, 5, 6, 9]
    >>> heap_sort(["banana", "apple", "cherry", "date"])
    ['apple', 'banana', 'cherry', 'date']
    """
    result = list(arr)
    n = len(result)

    if n <= 1:
        return result

    # Step 1: Build heap (O(n) time)
    heapify(result, reverse=reverse)

    # Step 2: Extract elements one by one from heap (O(n log n) time)
    for i in range(n - 1, 0, -1):
        # Move current root (max/min) to end
        result[0], result[i] = result[i], result[0]
        # Call sift_down on reduced heap
        _sift_down(result, i, 0, reverse=reverse)

    return result


class PriorityQueue(Generic[T]):
    """
    Priority Queue implementation backed by a Binary Heap.

    >>> pq = PriorityQueue()
    >>> pq.push("task1", priority=3)
    >>> pq.push("task2", priority=1)
    >>> pq.push("task3", priority=5)
    >>> pq.pop()  # Highest priority first
    'task3'
    >>> pq.pop()
    'task1'
    >>> len(pq)
    1
    """

    def __init__(self) -> None:
        """Initialize an empty Priority Queue."""
        self._heap: list[tuple[Any, T]] = []

    def is_empty(self) -> bool:
        """Return True if Priority Queue is empty."""
        return len(self._heap) == 0

    def __len__(self) -> int:
        """Return number of items in Priority Queue."""
        return len(self._heap)

    def push(self, item: T, priority: float) -> None:
        """Push item with given numeric priority."""
        entry = (priority, item)
        self._heap.append(entry)
        self._sift_up(len(self._heap) - 1)

    def pop(self) -> T:
        """Pop item with the highest priority."""
        if self.is_empty():
            raise IndexError("Cannot pop from empty PriorityQueue")
        
        # Swap root with last element
        self._heap[0], self._heap[-1] = self._heap[-1], self._heap[0]
        _, item = self._heap.pop()
        
        if not self.is_empty():
            self._sift_down(0)
            
        return item

    def peek(self) -> T:
        """Peek at item with the highest priority without removing it."""
        if self.is_empty():
            raise IndexError("Cannot peek into empty PriorityQueue")
        return self._heap[0][1]

    def _sift_up(self, idx: int) -> None:
        while idx > 0:
            parent = (idx - 1) // 2
            if self._heap[idx][0] > self._heap[parent][0]:
                self._heap[idx], self._heap[parent] = self._heap[parent], self._heap[idx]
                idx = parent
            else:
                break

    def _sift_down(self, idx: int) -> None:
        n = len(self._heap)
        while True:
            largest = idx
            left = 2 * idx + 1
            right = 2 * idx + 2

            if left < n and self._heap[left][0] > self._heap[largest][0]:
                largest = left
            if right < n and self._heap[right][0] > self._heap[largest][0]:
                largest = right

            if largest != idx:
                self._heap[idx], self._heap[largest] = self._heap[largest], self._heap[idx]
                idx = largest
            else:
                break


if __name__ == "__main__":
    import doctest

    print("Running Heap Sort doctests...")
    results = doctest.testmod()
    if results.failed == 0:
        print(f"✅ All {results.attempted} tests passed!")
    else:
        print(f"❌ {results.failed} tests failed out of {results.attempted}")
