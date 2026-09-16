"""
Suffix Array & Kasai's LCP Array Implementation in Python.

A Suffix Array is a sorted array of all suffixes of a given string.
Combined with Kasai's Longest Common Prefix (LCP) array, it allows efficient string processing:
- Substring Pattern Matching in O(M log N) time
- Counting Distinct Substrings in O(N) time using LCP
- Longest Repeated Substring in O(N) time

Complexity Analysis:
- Suffix Array Construction: O(N log^2 N) or O(N log N)
- Kasai's LCP Array Construction: O(N) time
- Space Complexity: O(N)
"""

from typing import List, Tuple


class SuffixArray:
    """
    Suffix Array and LCP Array generator.

    >>> sa = SuffixArray("banana")
    >>> sa.suffixes
    [5, 3, 1, 0, 4, 2]
    >>> sa.lcp
    [0, 1, 3, 0, 0, 2]
    >>> sa.count_distinct_substrings()
    15
    """

    def __init__(self, text: str):
        self.text = text
        self.n = len(text)
        self.suffixes: List[int] = self._build_suffix_array()
        self.lcp: List[int] = self._build_lcp_array() if self.n > 0 else []

    def _build_suffix_array(self) -> List[int]:
        """Construct Suffix Array in O(N log^2 N) time using prefix doubling."""
        n = self.n
        if n == 0:
            return []

        # Rank array: initial rank based on ASCII values
        rank = [ord(c) for c in self.text]
        sa = list(range(n))
        tmp = [0] * n

        k = 1
        while k < n:
            # Sort suffixes by tuple of ranks: (rank[i], rank[i + k])
            sa.sort(key=lambda i: (rank[i], rank[i + k] if i + k < n else -1))

            tmp[sa[0]] = 0
            for i in range(1, n):
                prev_rank = (rank[sa[i - 1]], rank[sa[i - 1] + k] if sa[i - 1] + k < n else -1)
                curr_rank = (rank[sa[i]], rank[sa[i] + k] if sa[i] + k < n else -1)
                tmp[sa[i]] = tmp[sa[i - 1]] + (1 if curr_rank != prev_rank else 0)

            rank, tmp = tmp, rank
            if rank[sa[n - 1]] == n - 1:
                break
            k *= 2

        return sa

    def _build_lcp_array(self) -> List[int]:
        """Construct Longest Common Prefix (LCP) array in O(N) time using Kasai's algorithm."""
        n = self.n
        sa = self.suffixes
        rank = [0] * n
        for i in range(n):
            rank[sa[i]] = i

        lcp = [0] * n
        h = 0
        for i in range(n):
            if rank[i] > 0:
                j = sa[rank[i] - 1]
                while i + h < n and j + h < n and self.text[i + h] == self.text[j + h]:
                    h += 1
                lcp[rank[i]] = h
                if h > 0:
                    h -= 1
        return lcp

    def count_distinct_substrings(self) -> int:
        """
        Calculate the total number of distinct non-empty substrings in O(N) time.
        Formula: Total Substrings N(N+1)/2 - Sum(LCP).
        """
        if self.n == 0:
            return 0
        total_substrings = self.n * (self.n + 1) // 2
        lcp_sum = sum(self.lcp)
        return total_substrings - lcp_sum

    def search_pattern(self, pattern: str) -> List[int]:
        """
        Find all starting indices of `pattern` in `text` in O(M log N) time using binary search.
        """
        m = len(pattern)
        if m == 0 or self.n == 0:
            return []

        # Find lower bound
        low, high = 0, self.n - 1
        first = -1
        while low <= high:
            mid = (low + high) // 2
            suffix = self.text[self.suffixes[mid] : self.suffixes[mid] + m]
            if suffix >= pattern:
                first = mid
                high = mid - 1
            else:
                low = mid + 1

        if first == -1 or not self.text[self.suffixes[first] :].startswith(pattern):
            return []

        # Find upper bound
        low, high = first, self.n - 1
        last = first
        while low <= high:
            mid = (low + high) // 2
            if self.text[self.suffixes[mid] :].startswith(pattern):
                last = mid
                low = mid + 1
            else:
                high = mid - 1

        matches = [self.suffixes[i] for i in range(first, last + 1)]
        return sorted(matches)


if __name__ == "__main__":
    import doctest

    results = doctest.testmod()
    if results.failed == 0:
        print(f"All {results.attempted} Suffix Array doctests passed successfully!")
