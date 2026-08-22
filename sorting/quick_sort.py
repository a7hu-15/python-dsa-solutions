from __future__ import annotations

"""
Quick Sort Algorithm

Quick Sort is a divide-and-conquer algorithm that picks a 'pivot' element,
partitions the array around the pivot, and recursively sorts the sub-arrays.

Time Complexity:
    - Best:    O(n log n) — balanced partitions
    - Average: O(n log n)
    - Worst:   O(n²)     — already sorted or all equal elements

Space Complexity: O(log n) — recursive call stack

Stability: Not stable — equal elements may change relative order.

>>> quick_sort([10, 7, 8, 9, 1, 5])
[1, 5, 7, 8, 9, 10]

>>> quick_sort([])
[]

>>> quick_sort([1])
[1]

>>> quick_sort([3, 3, 3])
[3, 3, 3]

>>> quick_sort([5, 4, 3, 2, 1])
[1, 2, 3, 4, 5]

>>> quick_sort([-5, -2, -8, 0, 3])
[-8, -5, -2, 0, 3]

>>> quick_sort([1.5, 0.5, 2.5, 1.0])
[0.5, 1.0, 1.5, 2.5]
"""

import random


def quick_sort(array: list) -> list:
    """
    Sort a list using the quick sort algorithm (returns a new sorted list).

    Uses the Lomuto partition scheme with random pivot selection
    to avoid worst-case behavior on sorted inputs.

    Args:
        array: A list of comparable elements to sort.

    Returns:
        A new sorted list.

    >>> quick_sort([64, 34, 25, 12, 22, 11, 90])
    [11, 12, 22, 25, 34, 64, 90]
    """
    if len(array) <= 1:
        return array

    pivot = random.choice(array)
    less = [x for x in array if x < pivot]
    equal = [x for x in array if x == pivot]
    greater = [x for x in array if x > pivot]

    return quick_sort(less) + equal + quick_sort(greater)


def quick_sort_in_place(
    array: list, low: int = 0, high: int | None = None
) -> None:
    """
    Sort a list in-place using quick sort with the Hoare partition scheme.

    Args:
        array: The list to sort (modified in-place).
        low: Starting index (inclusive).
        high: Ending index (inclusive). Defaults to len(array) - 1.

    >>> arr = [10, 7, 8, 9, 1, 5]
    >>> quick_sort_in_place(arr)
    >>> arr
    [1, 5, 7, 8, 9, 10]

    >>> arr = [3, 1, 2]
    >>> quick_sort_in_place(arr)
    >>> arr
    [1, 2, 3]
    """
    if high is None:
        high = len(array) - 1

    if low < high:
        pivot_index = _partition(array, low, high)
        quick_sort_in_place(array, low, pivot_index)
        quick_sort_in_place(array, pivot_index + 1, high)


def _partition(array: list, low: int, high: int) -> int:
    """
    Hoare partition scheme — selects a random pivot and partitions the array.

    Elements smaller than the pivot go to the left, larger to the right.

    Args:
        array: The list to partition.
        low: Starting index.
        high: Ending index.

    Returns:
        The partition index.
    """
    # Randomized pivot to avoid worst-case on sorted arrays
    pivot_idx = random.randint(low, high)
    pivot = array[pivot_idx]

    i = low - 1
    j = high + 1

    while True:
        i += 1
        while array[i] < pivot:
            i += 1

        j -= 1
        while array[j] > pivot:
            j -= 1

        if i >= j:
            return j

        array[i], array[j] = array[j], array[i]


def quick_sort_three_way(array: list) -> list:
    """
    Three-way quick sort (Dutch National Flag partitioning).

    Handles arrays with many duplicate elements efficiently.

    Args:
        array: A list of comparable elements.

    Returns:
        A new sorted list.

    >>> quick_sort_three_way([4, 2, 2, 8, 3, 3, 1])
    [1, 2, 2, 3, 3, 4, 8]

    >>> quick_sort_three_way([1, 1, 1, 1])
    [1, 1, 1, 1]
    """
    if len(array) <= 1:
        return list(array)

    arr = list(array)
    _three_way_partition(arr, 0, len(arr) - 1)
    return arr


def _three_way_partition(array: list, low: int, high: int) -> None:
    """
    In-place three-way partitioning for quick sort.

    Divides array into three parts: < pivot, == pivot, > pivot.

    Args:
        array: The list to partition.
        low: Starting index.
        high: Ending index.
    """
    if low >= high:
        return

    pivot = array[random.randint(low, high)]
    lt = low       # array[low..lt-1] < pivot
    gt = high      # array[gt+1..high] > pivot
    i = low        # array[lt..i-1] == pivot

    while i <= gt:
        if array[i] < pivot:
            array[lt], array[i] = array[i], array[lt]
            lt += 1
            i += 1
        elif array[i] > pivot:
            array[gt], array[i] = array[i], array[gt]
            gt -= 1
        else:
            i += 1

    _three_way_partition(array, low, lt - 1)
    _three_way_partition(array, gt + 1, high)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # Demo
    sample = [10, 7, 8, 9, 1, 5]
    print(f"Original:      {sample}")
    print(f"Quick Sort:    {quick_sort(sample)}")

    # In-place version
    sample2 = [64, 34, 25, 12, 22, 11, 90]
    print(f"\nOriginal:      {sample2}")
    quick_sort_in_place(sample2)
    print(f"In-place:      {sample2}")

    # Three-way version
    sample3 = [4, 2, 2, 8, 3, 3, 1, 1, 5, 5]
    print(f"\nOriginal:      {sample3}")
    print(f"Three-way:     {quick_sort_three_way(sample3)}")
