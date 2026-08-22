from __future__ import annotations

"""
Interpolation Search Algorithm

Interpolation Search is an improved variant of binary search for UNIFORMLY
DISTRIBUTED sorted arrays. Instead of always going to the middle, it estimates
the position of the target based on the value's proportional position.

Think of it like how you'd search a phone book — if looking for "Smith",
you'd open near the end, not the middle.

Time Complexity:
    - Best:    O(1)
    - Average: O(log log n) — for uniformly distributed data
    - Worst:   O(n)         — for non-uniform data

Space Complexity:
    - Iterative: O(1)
    - Recursive: O(log log n) average

Prerequisite: The array MUST be sorted. Works best with uniformly distributed values.

>>> interpolation_search([10, 20, 30, 40, 50, 60, 70, 80, 90, 100], 70)
6

>>> interpolation_search([10, 20, 30, 40, 50, 60, 70, 80, 90, 100], 55)
-1

>>> interpolation_search([], 5)
-1

>>> interpolation_search([42], 42)
0

>>> interpolation_search([42], 99)
-1

>>> interpolation_search([1, 1, 1, 1, 1], 1)
0
"""


def interpolation_search(array: list, target) -> int:
    """
    Iterative interpolation search.

    Uses the formula:
        pos = low + ((target - array[low]) * (high - low)) // (array[high] - array[low])

    to estimate the likely position of the target.

    Args:
        array: A sorted list of numeric elements.
        target: The number to search for.

    Returns:
        The index of the target if found, otherwise -1.

    >>> interpolation_search([2, 4, 6, 8, 10, 12, 14, 16], 10)
    4

    >>> interpolation_search([2, 4, 6, 8, 10, 12, 14, 16], 7)
    -1
    """
    low = 0
    high = len(array) - 1

    while low <= high and array[low] <= target <= array[high]:
        # Avoid division by zero when all elements are the same
        if array[high] == array[low]:
            if array[low] == target:
                return low
            return -1

        # Estimate position using interpolation formula
        pos = low + ((target - array[low]) * (high - low)) // (array[high] - array[low])

        if array[pos] == target:
            return pos
        elif array[pos] < target:
            low = pos + 1
        else:
            high = pos - 1

    return -1


def interpolation_search_recursive(
    array: list, target, low: int = 0, high: int | None = None
) -> int:
    """
    Recursive interpolation search.

    Args:
        array: A sorted list of numeric elements.
        target: The number to search for.
        low: Starting index (inclusive).
        high: Ending index (inclusive).

    Returns:
        The index of the target if found, otherwise -1.

    >>> interpolation_search_recursive([10, 20, 30, 40, 50], 30)
    2

    >>> interpolation_search_recursive([10, 20, 30, 40, 50], 25)
    -1
    """
    if high is None:
        high = len(array) - 1

    if low > high or not array:
        return -1

    if target < array[low] or target > array[high]:
        return -1

    if array[high] == array[low]:
        if array[low] == target:
            return low
        return -1

    # Interpolation formula
    pos = low + ((target - array[low]) * (high - low)) // (array[high] - array[low])

    if pos < low or pos > high:
        return -1

    if array[pos] == target:
        return pos
    elif array[pos] < target:
        return interpolation_search_recursive(array, target, pos + 1, high)
    else:
        return interpolation_search_recursive(array, target, low, pos - 1)


if __name__ == "__main__":
    import doctest

    doctest.testmod()

    # Demo — works great with uniformly distributed data
    uniform_data = list(range(10, 101, 10))  # [10, 20, 30, ..., 100]
    print(f"Array: {uniform_data}")

    targets = [30, 70, 100, 55]
    for t in targets:
        idx = interpolation_search(uniform_data, t)
        status = f"found at index {idx}" if idx != -1 else "not found"
        print(f"  Search for {t}: {status}")

    # Comparison with binary search
    print("\n--- Performance Note ---")
    print("For uniformly distributed data, interpolation search")
    print("typically finds elements in O(log log n) vs O(log n) for binary search.")
