"""
Unit tests for Johnson's All-Pairs Shortest Path algorithm implementation.
"""

import math
import pytest
from graphs.johnson_shortest_paths import JohnsonShortestPaths


def test_johnson_basic_graph():
    """Test Johnson's algorithm on a graph with non-negative edge weights."""
    graph = JohnsonShortestPaths(4)
    graph.add_edge(0, 1, 3.0)
    graph.add_edge(0, 3, 7.0)
    graph.add_edge(1, 2, 1.0)
    graph.add_edge(2, 3, 2.0)

    dist = graph.compute_all_pairs_shortest_paths()

    assert dist[0][0] == 0.0
    assert dist[0][1] == 3.0
    assert dist[0][2] == 4.0
    assert dist[0][3] == 6.0  # 0 -> 1 -> 2 -> 3 = 3 + 1 + 2 = 6
    assert dist[1][3] == 3.0
    assert dist[3][0] == math.inf  # Unreachable


def test_johnson_negative_weights():
    """Test Johnson's algorithm on a graph containing negative edge weights but no negative cycles."""
    graph = JohnsonShortestPaths(4)
    graph.add_edge(0, 1, -5.0)
    graph.add_edge(0, 2, 2.0)
    graph.add_edge(1, 2, 4.0)
    graph.add_edge(2, 3, 1.0)
    graph.add_edge(1, 3, 8.0)

    dist = graph.compute_all_pairs_shortest_paths()

    assert dist[0][0] == 0.0
    assert dist[0][1] == -5.0
    assert dist[0][2] == -1.0  # 0 -> 1 -> 2 = -5 + 4 = -1
    assert dist[0][3] == 0.0   # 0 -> 1 -> 2 -> 3 = -5 + 4 + 1 = 0


def test_johnson_negative_cycle():
    """Test that a negative-weight cycle raises a ValueError."""
    graph = JohnsonShortestPaths(3)
    graph.add_edge(0, 1, 1.0)
    graph.add_edge(1, 2, -3.0)
    graph.add_edge(2, 0, 1.0)  # Cycle 0->1->2->0 has sum 1 - 3 + 1 = -1

    with pytest.raises(ValueError, match="negative-weight cycle"):
        graph.compute_all_pairs_shortest_paths()


def test_johnson_disconnected_graph():
    """Test Johnson's algorithm on a disconnected graph."""
    graph = JohnsonShortestPaths(3)
    graph.add_edge(0, 1, 2.0)

    dist = graph.compute_all_pairs_shortest_paths()

    assert dist[0][1] == 2.0
    assert dist[1][0] == math.inf
    assert dist[0][2] == math.inf
    assert dist[2][0] == math.inf


def test_johnson_invalid_vertex():
    """Test out-of-bounds vertex handling."""
    graph = JohnsonShortestPaths(2)
    with pytest.raises(ValueError):
        graph.add_edge(0, 5, 1.0)

    with pytest.raises(ValueError):
        JohnsonShortestPaths(0)
