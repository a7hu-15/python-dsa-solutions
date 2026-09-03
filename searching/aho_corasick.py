from __future__ import annotations

"""
Aho-Corasick Multi-Pattern String Searching Automaton

The Aho-Corasick algorithm constructs a finite-state machine (Trie enhanced with
suffix failure links and output links) from a dictionary of target patterns. It finds
all occurrences of any pattern in an input text in linear time O(n + m + z), where:
- n = len(text)
- m = sum of lengths of all patterns
- z = number of pattern occurrences in text

Time Complexity:
    - Precomputation (Trie + BFS Links): O(m)
    - Search Phase:                      O(n + z)

Space Complexity:
    - O(m * |Sigma|) where |Sigma| is the alphabet size

>>> aho_corasick_search("ushers", ["he", "she", "his", "hers"])
{'he': [2], 'she': [1], 'hers': [2]}
"""

from collections import deque
import unittest
from typing import Dict, List, Tuple


def aho_corasick_search(text: str, patterns: List[str]) -> Dict[str, List[int]]:
    """
    Search for occurrences of multiple pattern keywords in text.

    Args:
        text: Target input string.
        patterns: List of pattern strings to match.

    Returns:
        Dict mapping each matching pattern to its list of starting indices.

    >>> aho_corasick_search("AABAACAADAABAABA", ["AABA", "AA"])
    {'AA': [0, 3, 6, 9, 12], 'AABA': [0, 9, 12]}
    """
    ac = AhoCorasick(patterns)
    return ac.search(text)


class TrieNode:
    """Node in Aho-Corasick Trie Automaton."""

    def __init__(self) -> None:
        self.children: Dict[str, TrieNode] = {}
        self.fail: TrieNode | None = None
        self.output: List[str] = []


class AhoCorasick:
    """Aho-Corasick String Matching Automaton."""

    def __init__(self, keywords: List[str] | None = None) -> None:
        self.root = TrieNode()
        self.is_built = False
        if keywords:
            for kw in keywords:
                self.add_pattern(kw)
            self.build()

    def add_pattern(self, pattern: str) -> None:
        """Add a pattern keyword to the trie."""
        if not pattern:
            return
        node = self.root
        for char in pattern:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.output.append(pattern)
        self.is_built = False

    def build(self) -> None:
        """Build failure and output links using Breadth-First Search (BFS)."""
        queue: deque[TrieNode] = deque()

        # Depth 1 nodes fail back to root
        for child in self.root.children.values():
            child.fail = self.root
            queue.append(child)

        while queue:
            curr = queue.popleft()

            for char, child in curr.children.items():
                # Traverse fail links to find longest proper suffix match
                fail_node = curr.fail
                while fail_node is not None and char not in fail_node.children:
                    fail_node = fail_node.fail

                if fail_node is None:
                    child.fail = self.root
                else:
                    child.fail = fail_node.children[char]
                    child.output.extend(child.fail.output)

                queue.append(child)

        self.is_built = True

    def search_all(self, text: str) -> List[Tuple[int, str]]:
        """
        Search text for all pattern matches.

        Args:
            text: Input string.

        Returns:
            List of tuples (end_index, pattern) for every match.
        """
        if not self.is_built:
            self.build()

        results: List[Tuple[int, str]] = []
        curr: TrieNode | None = self.root

        for i, char in enumerate(text):
            while curr is not None and char not in curr.children:
                curr = curr.fail

            if curr is None:
                curr = self.root
                continue

            curr = curr.children[char]
            for pattern in curr.output:
                results.append((i - len(pattern) + 1, pattern))

        return results

    def search(self, text: str) -> Dict[str, List[int]]:
        """
        Search text and return dictionary mapping each pattern to its list of start indices.

        Args:
            text: Input string.

        Returns:
            Dict mapping pattern -> list of 0-based starting indices.
        """
        matches = self.search_all(text)
        pattern_map: Dict[str, List[int]] = {}
        
        # Collect matches into mapping
        for start_idx, pattern in matches:
            if pattern not in pattern_map:
                pattern_map[pattern] = []
            pattern_map[pattern].append(start_idx)

        return pattern_map


class TestAhoCorasick(unittest.TestCase):
    """Unit test suite for Aho-Corasick multi-pattern automaton."""

    def test_basic_matching(self) -> None:
        ac = AhoCorasick(["he", "she", "his", "hers"])
        matches = ac.search("ushers")
        self.assertEqual(matches.get("she", []), [1])
        self.assertEqual(matches.get("he", []), [2])
        self.assertEqual(matches.get("hers", []), [2])
        self.assertEqual(matches.get("his", []), [])

    def test_overlapping_patterns(self) -> None:
        ac = AhoCorasick(["a", "aa", "aaa"])
        res = ac.search_all("aaaa")
        self.assertEqual(len(res), 9)  # 4 'a', 3 'aa', 2 'aaa'

    def test_no_matches(self) -> None:
        ac = AhoCorasick(["apple", "banana"])
        self.assertEqual(ac.search_all("orange grape"), [])

    def test_empty_inputs(self) -> None:
        ac = AhoCorasick([])
        self.assertEqual(ac.search_all("text"), [])
        ac2 = AhoCorasick(["test"])
        self.assertEqual(ac2.search_all(""), [])


if __name__ == "__main__":
    import doctest

    doctest_result = doctest.testmod()
    if doctest_result.failed == 0:
        print(f"Doctests passed: {doctest_result.attempted} tests run.")

    unittest.main()
