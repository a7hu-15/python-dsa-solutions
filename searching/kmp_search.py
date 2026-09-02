from __future__ import annotations

"""
Knuth-Morris-Pratt (KMP) String Searching Algorithm

The KMP algorithm searches for occurrences of a "pattern" string within a "text" string
by employing the observation that when a mismatch occurs, the pattern itself contains
sufficient information to determine where the next match could begin, avoiding re-examining
previously matched characters.

Algorithm Overview:
1. Precompute the Longest Prefix Suffix (LPS) array for the pattern.
   LPS[i] stores the length of the longest proper prefix of pattern[0..i] that is also a suffix of pattern[0..i].
2. Use the LPS array during text traversal to shift the pattern efficiently whenever a mismatch occurs.

Time Complexity:
    - Precomputation (LPS): O(m) where m = len(pattern)
    - Search Phase:         O(n) where n = len(text)
    - Total Time:           O(n + m)

Space Complexity:
    - O(m) to store the LPS array

>>> compute_lps("AAACAAAA")
[0, 1, 2, 0, 1, 2, 3, 3]

>>> kmp_search("ABABDABACDABABCABAB", "ABABCABAB")
[10]

>>> kmp_search("AAAAA", "AA")
[0, 1, 2, 3]

>>> kmp_search_first("ABABDABACDABABCABAB", "ABABCABAB")
10

>>> count_pattern_occurrences("ABABAB", "ABA")
2
"""

import unittest
from typing import List


def compute_lps(pattern: str) -> List[int]:
    """
    Compute the Longest Prefix Suffix (LPS) array for a given pattern string.

    LPS[i] is the length of the longest proper prefix of pattern[0..i]
    that is also a suffix of pattern[0..i].

    Args:
        pattern: The pattern string.

    Returns:
        List of integers representing the LPS array.

    >>> compute_lps("ABCDABD")
    [0, 0, 0, 0, 1, 2, 0]

    >>> compute_lps("AAAA")
    [0, 1, 2, 3]

    >>> compute_lps("")
    []
    """
    m = len(pattern)
    if m == 0:
        return []

    lps = [0] * m
    length = 0  # Length of the previous longest prefix suffix
    i = 1

    while i < m:
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1

    return lps


def kmp_search(text: str, pattern: str) -> List[int]:
    """
    Find all starting indices of pattern in text using KMP algorithm.

    Args:
        text: The string to search within.
        pattern: The substring to search for.

    Returns:
        List of 0-based starting indices where pattern matches text.

    >>> kmp_search("AABAACAADAABAABA", "AABA")
    [0, 9, 12]

    >>> kmp_search("HELLO WORLD", "WORLD")
    [6]

    >>> kmp_search("PYTHON", "JAVA")
    []

    >>> kmp_search("", "A")
    []

    >>> kmp_search("ABC", "")
    []
    """
    n = len(text)
    m = len(pattern)

    if m == 0 or n == 0 or m > n:
        return []

    lps = compute_lps(pattern)
    matches: List[int] = []

    i = 0  # Index for text
    j = 0  # Index for pattern

    while i < n:
        if pattern[j] == text[i]:
            i += 1
            j += 1

        if j == m:
            matches.append(i - j)
            j = lps[j - 1]
        elif i < n and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1

    return matches


def kmp_search_first(text: str, pattern: str) -> int:
    """
    Find the first starting index of pattern in text.

    Args:
        text: The string to search within.
        pattern: The substring to search for.

    Returns:
        Starting index of first match, or -1 if pattern is not found.

    >>> kmp_search_first("abcdefg", "cde")
    2

    >>> kmp_search_first("abcdefg", "xyz")
    -1
    """
    matches = kmp_search(text, pattern)
    return matches[0] if matches else -1


def count_pattern_occurrences(text: str, pattern: str) -> int:
    """
    Count the total number of pattern matches in text.

    Args:
        text: The string to search within.
        pattern: The pattern to count.

    Returns:
        Number of occurrences found.

    >>> count_pattern_occurrences("banana", "ana")
    2
    """
    return len(kmp_search(text, pattern))


class TestKMPSearch(unittest.TestCase):
    """Unit test cases for KMP string searching module."""

    def test_single_occurrence(self) -> None:
        self.assertEqual(kmp_search("hello world", "world"), [6])

    def test_multiple_occurrences(self) -> None:
        self.assertEqual(kmp_search("abracadabra", "ra"), [2, 9])

    def test_overlapping_matches(self) -> None:
        self.assertEqual(kmp_search("AAAAAA", "AAA"), [0, 1, 2, 3])

    def test_no_match(self) -> None:
        self.assertEqual(kmp_search("python programming", "java"), [])

    def test_pattern_equal_text(self) -> None:
        self.assertEqual(kmp_search("exactmatch", "exactmatch"), [0])

    def test_pattern_longer_than_text(self) -> None:
        self.assertEqual(kmp_search("short", "longertextpattern"), [])

    def test_empty_inputs(self) -> None:
        self.assertEqual(kmp_search("", "pattern"), [])
        self.assertEqual(kmp_search("text", ""), [])
        self.assertEqual(kmp_search("", ""), [])

    def test_lps_computation(self) -> None:
        self.assertEqual(compute_lps("ABACABA"), [0, 0, 1, 0, 1, 2, 3])
        self.assertEqual(compute_lps("A"), [0])


if __name__ == "__main__":
    import doctest

    doctest_result = doctest.testmod()
    if doctest_result.failed == 0:
        print(f"Doctests passed: {doctest_result.attempted} tests run.")

    unittest.main()
