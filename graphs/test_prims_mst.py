import unittest
from graphs.prims_mst import prims_mst


class TestPrimsMST(unittest.TestCase):
    def test_standard_graph(self):
        # 4 vertices, weighted edges
        edges = [
            (0, 1, 10),
            (0, 2, 6),
            (0, 3, 5),
            (1, 3, 15),
            (2, 3, 4),
        ]
        total_weight, mst_edges = prims_mst(4, edges, start_vertex=0)
        self.assertEqual(total_weight, 19)
        self.assertEqual(len(mst_edges), 3)

        # Normalized edges check
        norm_edges = sorted([(min(u, v), max(u, v), w) for u, v, w in mst_edges])
        self.assertEqual(norm_edges, [(0, 1, 10), (0, 3, 5), (2, 3, 4)])

    def test_single_vertex(self):
        total_weight, mst_edges = prims_mst(1, [])
        self.assertEqual(total_weight, 0)
        self.assertEqual(mst_edges, [])

    def test_start_vertex_flexibility(self):
        edges = [
            (0, 1, 2),
            (1, 2, 3),
            (0, 2, 8),
        ]
        # Start at vertex 0
        w0, _ = prims_mst(3, edges, start_vertex=0)
        # Start at vertex 2
        w2, _ = prims_mst(3, edges, start_vertex=2)
        self.assertEqual(w0, 5)
        self.assertEqual(w2, 5)

    def test_invalid_parameters(self):
        with self.assertRaises(ValueError):
            prims_mst(0, [])
        with self.assertRaises(ValueError):
            prims_mst(3, [], start_vertex=5)


if __name__ == "__main__":
    unittest.main()
