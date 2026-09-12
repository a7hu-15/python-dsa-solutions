import unittest
from data_structures.segment_tree_lazy import SegmentTreeLazy


class TestSegmentTreeLazy(unittest.TestCase):
    def test_basic_query_and_range_update(self):
        data = [1, 3, 5, 7, 9, 11]
        st = SegmentTreeLazy(data)

        # Initial range sum queries
        self.assertEqual(st.query_range(0, 5), 36)
        self.assertEqual(st.query_range(1, 3), 15)
        self.assertEqual(st.query_range(2, 2), 5)

        # Update range [1, 4] by adding 5
        st.update_range(1, 4, 5)  # Array becomes: [1, 8, 10, 12, 14, 11]
        self.assertEqual(st.query_range(0, 5), 56)
        self.assertEqual(st.query_range(1, 3), 30)
        self.assertEqual(st.query_range(4, 5), 25)

    def test_multiple_overlapping_updates(self):
        data = [0, 0, 0, 0, 0]
        st = SegmentTreeLazy(data)

        st.update_range(0, 2, 3)  # [3, 3, 3, 0, 0]
        st.update_range(1, 4, 2)  # [3, 5, 5, 2, 2]

        self.assertEqual(st.query_range(0, 0), 3)
        self.assertEqual(st.query_range(1, 2), 10)
        self.assertEqual(st.query_range(0, 4), 17)

    def test_single_element_array(self):
        st = SegmentTreeLazy([10])
        self.assertEqual(st.query_range(0, 0), 10)
        st.update_range(0, 0, -5)
        self.assertEqual(st.query_range(0, 0), 5)

    def test_out_of_bounds_queries(self):
        st = SegmentTreeLazy([1, 2, 3])
        self.assertEqual(st.query_range(-1, 5), 6)
        self.assertEqual(st.query_range(5, 10), 0)
        self.assertEqual(st.query_range(3, 1), 0)


if __name__ == "__main__":
    unittest.main()
