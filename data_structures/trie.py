"""
Trie (Prefix Tree) Data Structure Implementation

A Trie is a tree-like data structure used to efficiently store and retrieve keys
in a dataset of strings. It is widely used in autocomplete systems, spell checkers,
and IP routing tables.

Complexity:
    - Insert: O(L) time, where L is the length of the string.
    - Search: O(L) time.
    - StartsWith: O(L) time.
    - Delete: O(L) time.
    - Space: O(N * L) worst case, where N is number of words and L is average length.

>>> trie = Trie()
>>> trie.insert("apple")
>>> trie.insert("app")
>>> trie.insert("apricot")
>>> trie.search("apple")
True
>>> trie.search("app")
True
>>> trie.search("appl")
False
>>> trie.starts_with("ap")
True
>>> trie.starts_with("cat")
False
>>> trie.list_words_with_prefix("ap")
['app', 'apple', 'apricot']
>>> trie.count_words_with_prefix("ap")
3
>>> trie.delete("app")
True
>>> trie.search("app")
False
>>> trie.search("apple")
True
"""

from __future__ import annotations

from typing import Dict, List, Optional


class TrieNode:
    """Represents a single node in the Trie."""

    def __init__(self) -> None:
        self.children: Dict[str, TrieNode] = {}
        self.is_end_of_word: bool = False
        self.word_count: int = 0  # Number of words passing through this node


class Trie:
    """
    Trie (Prefix Tree) implementation supporting insertion, lookup, prefix matching,
    deletion, and autocomplete functionality.
    """

    def __init__(self) -> None:
        """Initialize an empty Trie."""
        self.root: TrieNode = TrieNode()

    def insert(self, word: str) -> None:
        """
        Insert a word into the Trie.

        Args:
            word: The string to insert.

        >>> t = Trie()
        >>> t.insert("hello")
        >>> t.search("hello")
        True
        """
        if not word:
            return

        current = self.root
        current.word_count += 1

        for char in word:
            if char not in current.children:
                current.children[char] = TrieNode()
            current = current.children[char]
            current.word_count += 1

        current.is_end_of_word = True

    def search(self, word: str) -> bool:
        """
        Check if a complete word exists in the Trie.

        Args:
            word: Word to search for.

        Returns:
            True if word exists, False otherwise.

        >>> t = Trie()
        >>> t.insert("python")
        >>> t.search("python")
        True
        >>> t.search("py")
        False
        """
        if not word:
            return False

        current = self.root
        for char in word:
            if char not in current.children:
                return False
            current = current.children[char]

        return current.is_end_of_word

    def starts_with(self, prefix: str) -> bool:
        """
        Check if there is any word in the Trie that starts with the given prefix.

        Args:
            prefix: Prefix to check.

        Returns:
            True if prefix matches at least one word, False otherwise.

        >>> t = Trie()
        >>> t.insert("algorithm")
        >>> t.starts_with("algo")
        True
        >>> t.starts_with("data")
        False
        """
        current = self.root
        for char in prefix:
            if char not in current.children:
                return False
            current = current.children[char]
        return True

    def count_words_with_prefix(self, prefix: str) -> int:
        """
        Return the total number of words sharing the given prefix.

        >>> t = Trie()
        >>> t.insert("cat")
        >>> t.insert("cater")
        >>> t.insert("catapult")
        >>> t.count_words_with_prefix("cat")
        3
        """
        current = self.root
        for char in prefix:
            if char not in current.children:
                return 0
            current = current.children[char]
        return current.word_count

    def list_words_with_prefix(self, prefix: str) -> List[str]:
        """
        Return all words in the Trie starting with the specified prefix (autocomplete).

        Args:
            prefix: Prefix to search for.

        Returns:
            List of matching words sorted alphabetically.

        >>> t = Trie()
        >>> t.insert("car")
        >>> t.insert("card")
        >>> t.insert("care")
        >>> t.list_words_with_prefix("car")
        ['car', 'card', 'care']
        """
        current = self.root
        for char in prefix:
            if char not in current.children:
                return []
            current = current.children[char]

        results: List[str] = []

        def _dfs(node: TrieNode, path: List[str]) -> None:
            if node.is_end_of_word:
                results.append(prefix + "".join(path))

            for char in sorted(node.children.keys()):
                _dfs(node.children[char], path + [char])

        _dfs(current, [])
        return results

    def delete(self, word: str) -> bool:
        """
        Delete a word from the Trie if present.

        Args:
            word: The word to delete.

        Returns:
            True if word was found and deleted, False otherwise.

        >>> t = Trie()
        >>> t.insert("code")
        >>> t.delete("code")
        True
        >>> t.search("code")
        False
        """
        if not self.search(word):
            return False

        def _delete_helper(node: TrieNode, word: str, depth: int) -> bool:
            node.word_count -= 1
            if depth == len(word):
                node.is_end_of_word = False
                return len(node.children) == 0

            char = word[depth]
            child_node = node.children[char]
            should_delete_child = _delete_helper(child_node, word, depth + 1)

            if should_delete_child:
                del node.children[char]
                return len(node.children) == 0 and not node.is_end_of_word

            return False

        _delete_helper(self.root, word, 0)
        return True


if __name__ == "__main__":
    import doctest

    print("Running Trie doctests...")
    results = doctest.testmod()
    if results.failed == 0:
        print(f"✅ All {results.attempted} tests passed!")
    else:
        print(f"❌ {results.failed} tests failed out of {results.attempted}")
