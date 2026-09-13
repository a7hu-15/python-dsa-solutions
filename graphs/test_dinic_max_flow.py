import unittest
from graphs.dinic_max_flow import Dinic


class TestDinicMaxFlow(unittest.TestCase):
    def test_standard_network(self):
        # 6-vertex flow network
        # 0 (source), 5 (sink)
        dinic = Dinic(6)
        dinic.add_edge(0, 1, 16)
        dinic.add_edge(0, 2, 13)
        dinic.add_edge(1, 2, 10)
        dinic.add_edge(1, 3, 12)
        dinic.add_edge(2, 1, 4)
        dinic.add_edge(2, 4, 14)
        dinic.add_edge(3, 2, 9)
        dinic.add_edge(3, 5, 20)
        dinic.add_edge(4, 3, 7)
        dinic.add_edge(4, 5, 4)

        max_flow = dinic.max_flow(0, 5)
        self.assertEqual(max_flow, 23)

    def test_disconnected_network(self):
        dinic = Dinic(4)
        dinic.add_edge(0, 1, 10)
        dinic.add_edge(2, 3, 10)
        self.assertEqual(dinic.max_flow(0, 3), 0)

    def test_single_edge_network(self):
        dinic = Dinic(2)
        dinic.add_edge(0, 1, 15)
        self.assertEqual(dinic.max_flow(0, 1), 15)

    def test_same_source_and_sink(self):
        dinic = Dinic(3)
        dinic.add_edge(0, 1, 10)
        self.assertEqual(dinic.max_flow(0, 0), 0)


if __name__ == "__main__":
    unittest.main()
