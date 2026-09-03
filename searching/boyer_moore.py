from __future__ import annotations

"""
Boyer-Moore String Searching Algorithm

The Boyer-Moore algorithm is an efficient string-searching algorithm that skips
sections of the text to achieve sub-linear time complexity in best cases. It compares
characters from right to left in the pattern and utilizes two heuristics:
1. Bad Character Rule: Shifts the pattern to align matched characters with the text.
2. Good Suffix Rule: Shifts the pattern based on matching suffix occurrences.

Time Complexity:
    - Best Case:   O(n / m) where n = len(text), m = len(pattern)
    - Worst Case:  O(n * m) without Good Suffix / O(n + m) with Good Suffix
    - Average:     O(n)

Space Complexity:
    - O(m + |Sigma|) where |Sigma| is the alphabet size (for bad character table)

>>> bad_character_table("NEEDLE")['E']
4

>>> boyer_moore_search("HERE IS A SIMPLE EXAMPLE", "EXAMPLE")
[17]

>>> boyer_moore_search("ABAAABCD", "ABC")
[4]

>>> boyer_moore_search_first("FIND THE NEEDLE IN HAYSTACK NEEDLE", "NEEDLE")
9
"""

import unittest
from typing import Dict, List


def bad_character_table(pattern: str) -> Dict[str, int]:
    """
    Build the Bad Character preprocessing table for the pattern.

    Stores the last occurrence index of each character in pattern except the last character.

    Args:
        pattern: The pattern string.

    Returns:
        Dictionary mapping characters to their last seen index in pattern.

    >>> bad_character_table("ABCD")
    {'A': 0, 'B': 1, 'C': 2}
    """
    table: Dict[str, int] = {}
    for i in range(len(pattern) - 1):
        table[pattern[i]] = i
    return table


def boyer_moore_search(text: str, pattern: str) -> List[int]:
    """
    Find all starting indices of pattern in text using the Boyer-Moore algorithm.

    Args:
        text: The text to search within.
        pattern: The pattern to search for.

    Returns:
        List of 0-based starting indices where pattern matches text.

    >>> boyer_moore_search("AABAACAADAABAABA", "AABA")
    [0, 9, 12]

    >>> boyer_moore_search("HELLO WORLD", "WORLD")
    [6]

    >>> boyer_moore_search("PYTHON", "JAVA")
    []

    >>> boyer_moore_search("", "TEST")
    []

    >>> boyer_moore_search("TEST", "")
    []
    """
    n = len(text)
    m = len(pattern)

    if m == 0 or n == 0 or m > n:
        return []

    bad_char = bad_character_table(pattern)
    matches: List[int] = []
    shift = 0

    while shift <= n - m:
        j = m - 1

        # Keep matching pattern and text backwards
        while j >= 0 and pattern[j] == text[shift + j]:
            j -= 1

        if j < 0:
            # Full match found
            matches.append(shift)
            # Shift pattern so that the next character in text aligns with its last occurrence in pattern
            if shift + m < n:
                shift += m - bad_char.get(text[shift + m], -1)
            else:
                shift += 1
        else:
            # Mismatch at pattern[j] and text[shift + j]
            bad_char_shift = j - bad_char.get(text[shift + j], -1)
            shift += max(1, bad_char_shift)

    return matches


def boyer_moore_search_first(text: str, pattern: str) -> int:
    """
    Find the first occurrence index of pattern in text.

    Args:
        text: Target text.
        pattern: Target pattern.

    Returns:
        0-based index of first match, or -1 if not found.

    >>> boyer_moore_search_first("abcdefgh", "def")
    3

    >>> boyer_moore_search_first("abcdefgh", "xyz")
    -1
    """
    matches = boyer_moore_search(text, pattern)
    return matches[0] if matches else -1


class TestBoyerMoore(unittest.TestCase):
    """Unit test suite for Boyer-Moore String Matching."""

    def test_single_match(self) -> None:
        self.assertEqual(boyer_moore_search("abacadabra", "cad"), [3])

    def test_multiple_matches(self) -> None:
        self.assertEqual(boyer_moore_search("AABAACAADAABAABA", "AABA"), [0, 9, 12])

    def test_no_match(self) -> None:
        self.assertEqual(boyer_moore_search("hello world", "python"), [])

    def test_pattern_equal_text(self) -> None:
        self.assertEqual(boyer_moore_search("match", "match"), [0])

    def test_pattern_longer_than_text(self) -> None:
        self.assertEqual(boyer_moore_search("short", "longerpattern"), [])

    def test_empty_string(self) -> None:
        self.assertEqual(boyer_moore_search("", "abc"), [])
        self.assertEqual(boyer_moore_search("abc", ""), [])

    def test_search_first(self) -> None:
        self.assertEqual(boyer_moore_search_first("banana", "ana"), 1)
        self.assertEqual(boyer_moore_search_first("banana", "apple"), -1)


if __name__ == "__main__":
    import doctest

    doctest_result = doctest.testmod()
    if doctest_result.failed == 0:
        print(f"Doctests passed: {doctest_result.attempted} tests run.")

    unittest.main()
