import unittest
from searching.rabin_karp import rabin_karp_search, rabin_karp_search_first


class TestRabinKarpSearch(unittest.TestCase):
    def test_single_occurrence(self):
        self.assertEqual(rabin_karp_search("hello world", "world"), [6])

    def test_multiple_occurrences(self):
        self.assertEqual(rabin_karp_search("abracadabra", "ra"), [2, 9])

    def test_overlapping_occurrences(self):
        self.assertEqual(rabin_karp_search("AAAAAA", "AAA"), [0, 1, 2, 3])

    def test_no_match(self):
        self.assertEqual(rabin_karp_search("python programming", "java"), [])

    def test_first_match_helper(self):
        self.assertEqual(rabin_karp_search_first("abcdefg", "cde"), 2)
        self.assertEqual(rabin_karp_search_first("abcdefg", "xyz"), -1)

    def test_edge_cases(self):
        self.assertEqual(rabin_karp_search("", "abc"), [])
        self.assertEqual(rabin_karp_search("abc", ""), [])
        self.assertEqual(rabin_karp_search("a", "abc"), [])


if __name__ == "__main__":
    unittest.main()
