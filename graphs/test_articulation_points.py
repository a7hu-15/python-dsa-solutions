import pytest
from graphs.articulation_points import GraphCutAnalyzer, find_cut_vertices_and_edges


def test_linear_path_graph():
    """Graph: 0 - 1 - 2 - 3"""
    edges = [(0, 1), (1, 2), (2, 3)]
    points, bridges = find_cut_vertices_and_edges(4, edges)

    assert points == {1, 2}
    assert set(bridges) == {(0, 1), (1, 2), (2, 3)}


def test_triangle_graph_no_cuts():
    """Graph: 0-1-2-0 (Cycle of length 3)"""
    edges = [(0, 1), (1, 2), (2, 0)]
    points, bridges = find_cut_vertices_and_edges(3, edges)

    assert points == set()
    assert bridges == []


def test_bridge_connected_triangles():
    """
    Two triangles connected by a bridge edge (2, 3):
    (0-1-2-0) - (3-4-5-3)
    """
    edges = [
        (0, 1), (1, 2), (2, 0),  # Triangle 1
        (2, 3),                  # Bridge
        (3, 4), (4, 5), (5, 3)   # Triangle 2
    ]
    points, bridges = find_cut_vertices_and_edges(6, edges)

    assert points == {2, 3}
    assert bridges == [(2, 3)]


def test_disconnected_graph():
    """Disconnected graph with separate components."""
    edges = [(0, 1), (1, 2)]  # Component 1: 0 - 1 - 2
    # Component 2: Isolated vertex 3
    points, bridges = find_cut_vertices_and_edges(4, edges)

    assert points == {1}
    assert set(bridges) == {(0, 1), (1, 2)}


def test_out_of_bounds_vertex():
    analyzer = GraphCutAnalyzer(3)
    with pytest.raises(ValueError):
        analyzer.add_edge(0, 5)
