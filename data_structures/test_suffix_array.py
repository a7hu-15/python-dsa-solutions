import unittest
from data_structures.suffix_array import SuffixArray


class TestSuffixArray(unittest.TestCase):
    def test_banana(self):
        sa = SuffixArray("banana")
        self.assertEqual(sa.suffixes, [5, 3, 1, 0, 4, 2])
        self.assertEqual(sa.lcp, [0, 1, 3, 0, 0, 2])
        self.assertEqual(sa.count_distinct_substrings(), 15)

    def test_pattern_search(self):
        sa = SuffixArray("abracadabra")
        matches = sa.search_pattern("abra")
        self.assertEqual(matches, [0, 7])

        matches_a = sa.search_pattern("a")
        self.assertEqual(matches_a, [0, 3, 5, 7, 10])

        self.assertEqual(sa.search_pattern("xyz"), [])

    def test_empty_string(self):
        sa = SuffixArray("")
        self.assertEqual(sa.suffixes, [])
        self.assertEqual(sa.lcp, [])
        self.assertEqual(sa.count_distinct_substrings(), 0)

    def test_single_character(self):
        sa = SuffixArray("a")
        self.assertEqual(sa.suffixes, [0])
        self.assertEqual(sa.lcp, [0])
        self.assertEqual(sa.count_distinct_substrings(), 1)


if __name__ == "__main__":
    unittest.main()
