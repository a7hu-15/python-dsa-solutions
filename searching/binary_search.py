from __future__ import annotations

"""
Binary Search Algorithm

Binary Search is a search algorithm that finds the position of a target value
within a SORTED array. It works by repeatedly dividing the search interval in half.

Time Complexity:
    - Best:    O(1)       — target is the middle element
    - Average: O(log n)
    - Worst:   O(log n)

Space Complexity:
    - Iterative: O(1)
    - Recursive: O(log n) — call stack

Prerequisite: The array MUST be sorted.

>>> binary_search([1, 3, 5, 7, 9, 11, 13], 7)
3

>>> binary_search([1, 3, 5, 7, 9, 11, 13], 1)
0

>>> binary_search([1, 3, 5, 7, 9, 11, 13], 13)
6

>>> binary_search([1, 3, 5, 7, 9, 11, 13], 6)
-1

>>> binary_search([], 5)
-1

>>> binary_search([42], 42)
0

>>> binary_search([42], 99)
-1
"""


def binary_search(array: list, target) -> int:
    """
    Iterative binary search.

    Args:
        array: A sorted list of comparable elements.
        target: The element to search for.

    Returns:
        The index of the target if found, otherwise -1.

    >>> binary_search([2, 4, 6, 8, 10], 6)
    2

    >>> binary_search([2, 4, 6, 8, 10], 5)
    -1
    """
    low = 0
    high = len(array) - 1

    while low <= high:
        mid = low + (high - low) // 2  # Avoids potential overflow

        if array[mid] == target:
            return mid
        elif array[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return -1


def binary_search_recursive(array: list, target, low: int = 0, high: int | None = None) -> int:
    """
    Recursive binary search.

    Args:
        array: A sorted list of comparable elements.
        target: The element to search for.
        low: Starting index (inclusive).
        high: Ending index (inclusive).

    Returns:
        The index of the target if found, otherwise -1.

    >>> binary_search_recursive([1, 3, 5, 7, 9], 5)
    2

    >>> binary_search_recursive([1, 3, 5, 7, 9], 4)
    -1
    """
    if high is None:
        high = len(array) - 1

    if low > high:
        return -1

    mid = low + (high - low) // 2

    if array[mid] == target:
        return mid
    elif array[mid] < target:
        return binary_search_recursive(array, target, mid + 1, high)
    else:
        return binary_search_recursive(array, target, low, mid - 1)


def binary_search_leftmost(array: list, target) -> int:
    """
    Find the leftmost (first) occurrence of target in a sorted array.

    Useful when the array contains duplicate elements.

    Args:
        array: A sorted list of comparable elements.
        target: The element to search for.

    Returns:
        The index of the leftmost occurrence, or -1 if not found.

    >>> binary_search_leftmost([1, 2, 2, 2, 3, 4], 2)
    1

    >>> binary_search_leftmost([1, 2, 2, 2, 3, 4], 5)
    -1

    >>> binary_search_leftmost([2, 2, 2], 2)
    0
    """
    low = 0
    high = len(array) - 1
    result = -1

    while low <= high:
        mid = low + (high - low) // 2

        if array[mid] == target:
            result = mid
            high = mid - 1  # Keep searching left
        elif array[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return result


def binary_search_rightmost(array: list, target) -> int:
    """
    Find the rightmost (last) occurrence of target in a sorted array.

    Args:
        array: A sorted list of comparable elements.
        target: The element to search for.

    Returns:
        The index of the rightmost occurrence, or -1 if not found.

    >>> binary_search_rightmost([1, 2, 2, 2, 3, 4], 2)
    3

    >>> binary_search_rightmost([1, 2, 2, 2, 3, 4], 5)
    -1

    >>> binary_search_rightmost([2, 2, 2], 2)
    2
    """
    low = 0
    high = len(array) - 1
    result = -1

    while low <= high:
        mid = low + (high - low) // 2

        if array[mid] == target:
            result = mid
            low = mid + 1  # Keep searching right
        elif array[mid] < target:
            low = mid + 1
        else:
            high = mid - 1

    return result


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # Demo
    sorted_array = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91]
    print(f"Array: {sorted_array}")
    print(f"Search for 23: index = {binary_search(sorted_array, 23)}")
    print(f"Search for 50: index = {binary_search(sorted_array, 50)}")

    # Duplicate handling
    dupes = [1, 3, 3, 3, 3, 5, 7]
    print(f"\nArray with dupes: {dupes}")
    print(f"Leftmost 3:  index = {binary_search_leftmost(dupes, 3)}")
    print(f"Rightmost 3: index = {binary_search_rightmost(dupes, 3)}")
