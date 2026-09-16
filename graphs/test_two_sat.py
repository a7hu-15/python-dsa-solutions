import unittest
from graphs.two_sat import TwoSAT


class TestTwoSAT(unittest.TestCase):
    def test_satisfiable_formula(self):
        # (x1 or x2) and (not x1 or x2) and (x1 or not x2)
        sat = TwoSAT(2)
        sat.add_clause(1, True, 2, True)
        sat.add_clause(1, False, 2, True)
        sat.add_clause(1, True, 2, False)

        self.assertTrue(sat.is_satisfiable())
        assignment = sat.get_assignment()
        self.assertTrue(assignment[1])
        self.assertTrue(assignment[2])

    def test_unsatisfiable_formula(self):
        # (x1 or x1) and (not x1 or not x1) -> Contradiction
        sat = TwoSAT(1)
        sat.add_clause(1, True, 1, True)
        sat.add_clause(1, False, 1, False)

        self.assertFalse(sat.is_satisfiable())
        self.assertEqual(sat.get_assignment(), {})

    def test_multiple_variables_satisfiable(self):
        # (x1 or x2) and (not x2 or x3) and (not x3 or not x1)
        sat = TwoSAT(3)
        sat.add_clause(1, True, 2, True)
        sat.add_clause(2, False, 3, True)
        sat.add_clause(3, False, 1, False)

        self.assertTrue(sat.is_satisfiable())


if __name__ == "__main__":
    unittest.main()
