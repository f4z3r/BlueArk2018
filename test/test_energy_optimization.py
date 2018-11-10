#!/usr/bin/env python3

"""Tests for the optimizer."""

import unittest

from blueark.optmization.opt import OptimizationProblem


class TestEquationParsing(unittest.TestCase):

    def test_use_case(self):
        """Performs a test on a simple predictible network."""

        matrix = [[1.0, 1.0, 0.0, 0.0],
                  [0.0, -1.0, 1.0, 0.0],
                  [1.0, 0.0, 1.0, -1.0],
                  [1.0, 0.0, 1.0, -1.0],
                  [0.0, 0.0, 1.0, 0.0]]

        rhs_vector = [100., 50., 0., 80., 100.]

        equlities = [0, 0, 0, 1, 1]

        g_efficieny = 1.0
        obj_function = [g_efficieny, 0.0, 0.0, 0.0]

        solver = OptimizationProblem(len(matrix[0]),
                                     matrix,
                                     rhs_vector,
                                     equlities,
                                     obj_function)

        solver.solve()

        self.assertEqual(solver.value, 80)


if __name__ == '__main__':
    tester = TestEquationParsing()
    tester.test_use_case()
