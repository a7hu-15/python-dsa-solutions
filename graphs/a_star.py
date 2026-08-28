"""
A* (A-Star) Pathfinding Algorithm on 2D Grid Networks.

A* is an informed search algorithm (best-first search) used for finding the shortest path between nodes.
It uses a distance heuristic h(n) combined with the exact path cost g(n) to prioritize node expansion:
    f(n) = g(n) + h(n)

Complexity Analysis:
- Time Complexity: O(E log V) in general, or O(B^D) worst-case where B is branching factor and D is depth.
- Space Complexity: O(V) to store open/closed set nodes and parent pointers.
"""

import heapq
import math
from typing import Dict, List, Optional, Set, Tuple

Point = Tuple[int, int]


def manhattan_distance(p1: Point, p2: Point) -> float:
    """Calculate Manhattan distance heuristic (|x1 - x2| + |y1 - y2|)."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def euclidean_distance(p1: Point, p2: Point) -> float:
    """Calculate Euclidean distance heuristic sqrt((x1 - x2)^2 + (y1 - y2)^2)."""
    return math.hypot(p1[0] - p2[0], p1[1] - p2[1])


def chebyshev_distance(p1: Point, p2: Point) -> float:
    """Calculate Chebyshev distance heuristic max(|x1 - x2|, |y1 - y2|)."""
    return max(abs(p1[0] - p2[0]), abs(p1[1] - p2[1]))


class AStarGrid:
    """
    2D Grid Pathfinding solver using A* algorithm.
    """

    def __init__(self, grid: List[List[int]], allow_diagonal: bool = False):
        """
        Initialize A* Grid solver.

        :param grid: 2D matrix where 0 represents walkable cell and 1 represents obstacle.
        :param allow_diagonal: Whether 8-directional movement is permitted.
        """
        self.grid = grid
        self.rows = len(grid)
        self.cols = len(grid[0]) if self.rows > 0 else 0
        self.allow_diagonal = allow_diagonal

    def _get_neighbors(self, p: Point) -> List[Tuple[Point, float]]:
        """Get valid adjacent coordinates and step movement cost."""
        r, c = p
        neighbors = []
        
        # 4-directional moves (up, down, left, right)
        cardinals = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in cardinals:
            nr, nc = r + dr, c + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] == 0:
                neighbors.append(((nr, nc), 1.0))

        if self.allow_diagonal:
            # 4-diagonal moves with cost sqrt(2)
            diagonals = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
            for dr, dc in diagonals:
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols and self.grid[nr][nc] == 0:
                    # Prevent diagonal cutting through adjacent blocked corners
                    if self.grid[r][nc] == 0 and self.grid[nr][c] == 0:
                        neighbors.append(((nr, nc), math.sqrt(2)))

        return neighbors

    def find_path(
        self, start: Point, goal: Point, heuristic=manhattan_distance
    ) -> Optional[Tuple[List[Point], float]]:
        """
        Execute A* search to find shortest path from start to goal.

        :param start: (row, col) start tuple.
        :param goal: (row, col) goal tuple.
        :param heuristic: Heuristic function taking (point, goal) -> float cost estimate.
        :return: Tuple of (path list, total path cost) or None if no path exists.
        """
        if not (0 <= start[0] < self.rows and 0 <= start[1] < self.cols):
            raise ValueError(f"Start point {start} outside grid bounds.")
        if not (0 <= goal[0] < self.rows and 0 <= goal[1] < self.cols):
            raise ValueError(f"Goal point {goal} outside grid bounds.")
        if self.grid[start[0]][start[1]] != 0 or self.grid[goal[0]][goal[1]] != 0:
            return None  # Start or goal is blocked

        # Priority queue stores tuples: (f_score, counter, point)
        counter = 0
        open_set: List[Tuple[float, int, Point]] = []
        heapq.heappush(open_set, (heuristic(start, goal), counter, start))

        came_from: Dict[Point, Point] = {}
        g_score: Dict[Point, float] = {start: 0.0}
        f_score: Dict[Point, float] = {start: heuristic(start, goal)}

        closed_set: Set[Point] = set()

        while open_set:
            _, _, current = heapq.heappop(open_set)

            if current == goal:
                # Reconstruct path
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                path.reverse()
                return path, g_score[goal]

            if current in closed_set:
                continue
            closed_set.add(current)

            for neighbor, cost in self._get_neighbors(current):
                if neighbor in closed_set:
                    continue

                tentative_g = g_score[current] + cost
                if tentative_g < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f = tentative_g + heuristic(neighbor, goal)
                    f_score[neighbor] = f
                    counter += 1
                    heapq.heappush(open_set, (f, counter, neighbor))

        return None

    def visualize_path(self, path: List[Point]) -> str:
        """Render ASCII string representation of grid with path (*), start (S), goal (G)."""
        path_set = set(path)
        start, goal = path[0], path[-1]
        lines = []

        for r in range(self.rows):
            row_chars = []
            for c in range(self.cols):
                p = (r, c)
                if p == start:
                    row_chars.append("S")
                elif p == goal:
                    row_chars.append("G")
                elif p in path_set:
                    row_chars.append("*")
                elif self.grid[r][c] == 1:
                    row_chars.append("█")
                else:
                    row_chars.append(".")
            lines.append(" ".join(row_chars))

        return "\n".join(lines)


if __name__ == "__main__":
    import unittest

    class TestAStar(unittest.TestCase):
        def test_simple_path(self):
            grid = [
                [0, 0, 0, 0],
                [1, 1, 0, 1],
                [0, 0, 0, 0],
                [0, 1, 1, 0],
            ]
            solver = AStarGrid(grid)
            result = solver.find_path((0, 0), (3, 3))
            self.assertIsNotNone(result)
            path, cost = result
            self.assertEqual(start := path[0], (0, 0))
            self.assertEqual(end := path[-1], (3, 3))
            self.assertEqual(cost, 6.0)

        def test_blocked_path(self):
            grid = [
                [0, 1, 0],
                [0, 1, 0],
                [0, 1, 0],
            ]
            solver = AStarGrid(grid)
            result = solver.find_path((0, 0), (0, 2))
            self.assertIsNone(result)

        def test_diagonal_movement(self):
            grid = [
                [0, 0, 0],
                [0, 0, 0],
                [0, 0, 0],
            ]
            solver = AStarGrid(grid, allow_diagonal=True)
            result = solver.find_path((0, 0), (2, 2), heuristic=euclidean_distance)
            self.assertIsNotNone(result)
            path, cost = result
            self.assertAlmostEqual(cost, 2 * math.sqrt(2), places=4)

    unittest.main()
