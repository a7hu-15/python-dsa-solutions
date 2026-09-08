import pytest
from graphs.floyd_warshall import FloydWarshall, floyd_warshall


def test_floyd_warshall_basic():
    # 0 -> 1 (4), 1 -> 2 (-2), 0 -> 2 (5)
    edges = [(0, 1, 4.0), (1, 2, -2.0), (0, 2, 5.0)]
    dist, neg_cycle = floyd_warshall(3, edges)

    assert not neg_cycle
    assert dist[0][1] == 4.0
    assert dist[1][2] == -2.0
    assert dist[0][2] == 2.0  # Path 0 -> 1 -> 2 is 4 + (-2) = 2


def test_floyd_warshall_path_reconstruction():
    fw = FloydWarshall(4)
    fw.add_edge(0, 1, 5)
    fw.add_edge(1, 2, 3)
    fw.add_edge(2, 3, 1)
    fw.compute_shortest_paths()

    path = fw.get_path(0, 3)
    assert path == [0, 1, 2, 3]


def test_floyd_warshall_negative_cycle():
    # 0 -> 1 (1), 1 -> 2 (-5), 2 -> 0 (2) => Total cycle weight = -2
    edges = [(0, 1, 1.0), (1, 2, -5.0), (2, 0, 2.0)]
    dist, neg_cycle = floyd_warshall(3, edges)
    assert neg_cycle


def test_floyd_warshall_out_of_bounds():
    fw = FloydWarshall(2)
    with pytest.raises(ValueError):
        fw.add_edge(0, 3, 10.0)
