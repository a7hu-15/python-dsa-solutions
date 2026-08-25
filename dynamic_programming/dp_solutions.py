"""Dynamic Programming Algorithms Implementation in Python.

This module provides implementations for classic Dynamic Programming problems:
1. 0/1 Knapsack Problem (with space optimization & reconstructed selected items)
2. Longest Common Subsequence (LCS)
3. Edit Distance (Levenshtein Distance)

All functions include comprehensive docstrings, complexity analysis, and doctests.
"""

from typing import List, Tuple


def knapsack_01(weights: List[int], values: List[int], capacity: int) -> Tuple[int, List[int]]:
    """Solves the 0/1 Knapsack problem.

    Given N items, each with a weight and a value, determine the maximum value
    that can be put into a knapsack of capacity W, and return the indices of
    the selected items.

    Time Complexity: O(N * W) where N is number of items and W is capacity.
    Space Complexity: O(N * W) for item tracking and table.

    >>> knapsack_01([2, 3, 4, 5], [3, 4, 5, 6], 5)
    (7, [0, 1])
    >>> knapsack_01([1, 2, 3], [10, 15, 40], 6)
    (65, [0, 1, 2])
    >>> knapsack_01([5, 4, 6], [10, 40, 30], 3)
    (0, [])
    """
    n = len(weights)
    if n == 0 or capacity <= 0:
        return 0, []

    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        w = weights[i - 1]
        v = values[i - 1]
        for c in range(1, capacity + 1):
            if w <= c:
                dp[i][c] = max(dp[i - 1][c], dp[i - 1][c - w] + v)
            else:
                dp[i][c] = dp[i - 1][c]

    max_value = dp[n][capacity]

    # Reconstruct selected items
    selected_items = []
    curr_c = capacity
    for i in range(n, 0, -1):
        if dp[i][curr_c] != dp[i - 1][curr_c]:
            selected_items.append(i - 1)
            curr_c -= weights[i - 1]

    selected_items.reverse()
    return max_value, selected_items


def longest_common_subsequence(text1: str, text2: str) -> Tuple[int, str]:
    """Finds the length and string representation of the Longest Common Subsequence (LCS).

    Time Complexity: O(M * N) where M and N are lengths of text1 and text2.
    Space Complexity: O(M * N) for DP table.

    >>> longest_common_subsequence("abcde", "ace")
    (3, 'ace')
    >>> longest_common_subsequence("abc", "abc")
    (3, 'abc')
    >>> longest_common_subsequence("abc", "def")
    (0, '')
    """
    m, n = len(text1), len(text2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1] + 1
            else:
                dp[i][j] = max(dp[i - 1][j], dp[i][j - 1])

    # Reconstruct LCS string
    lcs_chars = []
    i, j = m, n
    while i > 0 and j > 0:
        if text1[i - 1] == text2[j - 1]:
            lcs_chars.append(text1[i - 1])
            i -= 1
            j -= 1
        elif dp[i - 1][j] >= dp[i][j - 1]:
            i -= 1
        else:
            j -= 1

    lcs_chars.reverse()
    return dp[m][n], "".join(lcs_chars)


def edit_distance(str1: str, str2: str) -> int:
    """Calculates the minimum edit distance (Levenshtein Distance) between two strings.

    Operations allowed: Insert, Delete, Replace.

    Time Complexity: O(M * N)
    Space Complexity: O(M * N)

    >>> edit_distance("horse", "ros")
    3
    >>> edit_distance("intention", "execution")
    5
    >>> edit_distance("kitten", "sitting")
    3
    """
    m, n = len(str1), len(str2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]

    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j

    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if str1[i - 1] == str2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(
                    dp[i - 1][j],      # Delete
                    dp[i][j - 1],      # Insert
                    dp[i - 1][j - 1]   # Replace
                )

    return dp[m][n]


if __name__ == "__main__":
    import doctest

    results = doctest.testmod()
    print(f"Doctest results: {results}")
