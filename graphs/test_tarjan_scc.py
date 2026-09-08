import pytest
from graphs.tarjan_scc import TarjanSCC, find_strongly_connected_components


def test_simple_cycle_scc():
    edges = [(0, 1), (1, 2), (2, 0)]
    sccs = find_strongly_connected_components(3, edges)
    assert len(sccs) == 1
    assert sccs[0] == [0, 1, 2]


def test_dag_scc():
    # In a DAG, each vertex is its own SCC
    edges = [(0, 1), (1, 2), (0, 2)]
    sccs = find_strongly_connected_components(3, edges)
    assert len(sccs) == 3
    sorted_sccs = sorted(sccs)
    assert sorted_sccs == [[0], [1], [2]]


def test_multiple_components():
    # 0 -> 1 -> 2 -> 0, 2 -> 3, 3 -> 4 -> 3
    edges = [(0, 1), (1, 2), (2, 0), (2, 3), (3, 4), (4, 3)]
    sccs = find_strongly_connected_components(5, edges)
    assert len(sccs) == 2
    assert [0, 1, 2] in sccs
    assert [3, 4] in sccs


def test_out_of_bounds_and_empty():
    g = TarjanSCC(2)
    with pytest.raises(ValueError):
        g.add_edge(0, 5)

    g_empty = TarjanSCC(0)
    assert g_empty.find_sccs() == []
