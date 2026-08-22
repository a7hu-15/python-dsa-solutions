from __future__ import annotations

"""
Merge Sort Algorithm

Merge Sort is a divide-and-conquer algorithm that divides the input array
into two halves, recursively sorts them, and then merges the two sorted halves.

Time Complexity:
    - Best:    O(n log n)
    - Average: O(n log n)
    - Worst:   O(n log n)

Space Complexity: O(n) — requires auxiliary space for merging

Stability: Stable — equal elements maintain their relative order.

>>> merge_sort([38, 27, 43, 3, 9, 82, 10])
[3, 9, 10, 27, 38, 43, 82]

>>> merge_sort([])
[]

>>> merge_sort([1])
[1]

>>> merge_sort([5, 4, 3, 2, 1])
[1, 2, 3, 4, 5]

>>> merge_sort([1, 2, 3, 4, 5])
[1, 2, 3, 4, 5]

>>> merge_sort([-3, -1, -7, -4, 0, 2])
[-7, -4, -3, -1, 0, 2]

>>> merge_sort([3.1, 2.5, 4.8, 1.2])
[1.2, 2.5, 3.1, 4.8]
"""


def merge_sort(array: list) -> list:
    """
    Sort a list using the merge sort algorithm.

    Args:
        array: A list of comparable elements to sort.

    Returns:
        A new sorted list.

    >>> merge_sort([10, 9, 8, 7, 6])
    [6, 7, 8, 9, 10]
    """
    if len(array) <= 1:
        return array

    mid = len(array) // 2
    left_half = merge_sort(array[:mid])
    right_half = merge_sort(array[mid:])

    return _merge(left_half, right_half)


def _merge(left: list, right: list) -> list:
    """
    Merge two sorted lists into a single sorted list.

    Args:
        left: A sorted list.
        right: A sorted list.

    Returns:
        A merged sorted list.

    >>> _merge([1, 3, 5], [2, 4, 6])
    [1, 2, 3, 4, 5, 6]

    >>> _merge([], [1, 2])
    [1, 2]

    >>> _merge([1], [])
    [1]
    """
    result = []
    i = j = 0

    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1

    result.extend(left[i:])
    result.extend(right[j:])
    return result


def merge_sort_in_place(array: list, start: int = 0, end: int | None = None) -> None:
    """
    Sort a list in-place using merge sort (modifies the original list).

    Args:
        array: The list to sort.
        start: Starting index (inclusive).
        end: Ending index (exclusive). Defaults to len(array).

    >>> arr = [38, 27, 43, 3, 9, 82, 10]
    >>> merge_sort_in_place(arr)
    >>> arr
    [3, 9, 10, 27, 38, 43, 82]
    """
    if end is None:
        end = len(array)

    if end - start <= 1:
        return

    mid = (start + end) // 2
    merge_sort_in_place(array, start, mid)
    merge_sort_in_place(array, mid, end)

    # Merge in-place using temporary storage
    merged = []
    i, j = start, mid

    while i < mid and j < end:
        if array[i] <= array[j]:
            merged.append(array[i])
            i += 1
        else:
            merged.append(array[j])
            j += 1

    merged.extend(array[i:mid])
    merged.extend(array[j:end])

    array[start:end] = merged


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # Demo
    sample = [38, 27, 43, 3, 9, 82, 10]
    print(f"Original:  {sample}")
    print(f"Sorted:    {merge_sort(sample)}")

    # In-place version
    sample2 = [64, 34, 25, 12, 22, 11, 90]
    print(f"\nOriginal:  {sample2}")
    merge_sort_in_place(sample2)
    print(f"In-place:  {sample2}")
