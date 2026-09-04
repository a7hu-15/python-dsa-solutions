from __future__ import annotations

"""
Rabin-Karp String Searching Algorithm using Polynomial Rolling Hash.

The Rabin-Karp algorithm uses a rolling hash function to quickly check if a pattern string
matches any substring of a text string. If the hash values match, an explicit character check
is performed to prevent hash collision false positives.

Algorithm Overview:
1. Compute hash of the pattern and initial window of text of length M (len(pattern)).
2. Slide pattern over text one character at a time.
3. Update hash value in O(1) time using rolling hash formula:
   hash(i+1) = (d * (hash(i) - text[i] * h) + text[i+M]) % prime
4. If hash values match, compare characters.

Time Complexity:
    - Average / Best Case:  O(N + M) where N = len(text), M = len(pattern)
    - Worst Case:           O(N * M) (occurs when all hashes collide)

Space Complexity:
    - O(1) auxiliary space (excluding match index results list)

>>> rabin_karp_search("ABABDABACDABABCABAB", "ABABCABAB")
[10]

>>> rabin_karp_search("GEEKS FOR GEEKS", "GEEK")
[0, 10]

>>> rabin_karp_search("AAAAA", "AA")
[0, 1, 2, 3]

>>> rabin_karp_search_first("ABABDABACDABABCABAB", "ABABCABAB")
10
"""

from typing import List

# Default alphabet size (d = 256 for ASCII) and large prime modulus (q)
DEFAULT_ALPHABET_SIZE = 256
DEFAULT_PRIME_MODULUS = 101


def rabin_karp_search(
    text: str,
    pattern: str,
    alphabet_size: int = DEFAULT_ALPHABET_SIZE,
    prime: int = DEFAULT_PRIME_MODULUS,
) -> List[int]:
    """Finds all starting indices of pattern in text using Rabin-Karp rolling hash.

    Args:
        text: The text string to search in.
        pattern: The pattern substring to search for.
        alphabet_size: Number of unique characters in alphabet (default 256).
        prime: A prime number used for modulo arithmetic to prevent integer overflow (default 101).

    Returns:
        List of 0-based starting indices where pattern matches text.

    >>> rabin_karp_search("AABAACAADAABAABA", "AABA")
    [0, 9, 12]

    >>> rabin_karp_search("HELLO WORLD", "WORLD")
    [6]

    >>> rabin_karp_search("PYTHON", "JAVA")
    []

    >>> rabin_karp_search("", "A")
    []

    >>> rabin_karp_search("ABC", "")
    []
    """
    n = len(text)
    m = len(pattern)

    if m == 0 or n == 0 or m > n:
        return []

    matches: List[int] = []

    # High order multiplier value h = (alphabet_size ^ (m - 1)) % prime
    h = pow(alphabet_size, m - 1, prime)

    pattern_hash = 0
    text_hash = 0

    # Calculate initial hash value for pattern and first window of text
    for i in range(m):
        pattern_hash = (alphabet_size * pattern_hash + ord(pattern[i])) % prime
        text_hash = (alphabet_size * text_hash + ord(text[i])) % prime

    # Slide pattern window over text
    for i in range(n - m + 1):
        # Check if hash values match
        if pattern_hash == text_hash:
            # Explicit character-by-character verification on hash match
            if text[i : i + m] == pattern:
                matches.append(i)

        # Compute rolling hash for next window
        if i < n - m:
            text_hash = (alphabet_size * (text_hash - ord(text[i]) * h) + ord(text[i + m])) % prime
            # Ensure non-negative hash value
            if text_hash < 0:
                text_hash += prime

    return matches


def rabin_karp_search_first(
    text: str,
    pattern: str,
    alphabet_size: int = DEFAULT_ALPHABET_SIZE,
    prime: int = DEFAULT_PRIME_MODULUS,
) -> int:
    """Finds the first starting index of pattern in text, or -1 if not found.

    >>> rabin_karp_search_first("abcdefg", "cde")
    2

    >>> rabin_karp_search_first("abcdefg", "xyz")
    -1
    """
    matches = rabin_karp_search(text, pattern, alphabet_size, prime)
    return matches[0] if matches else -1


if __name__ == "__main__":
    import doctest

    results = doctest.testmod()
    print(f"Doctest results: {results}")
